from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import User, Payment, Booking, RentalPlan
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta


def register(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        name = request.POST.get('name')
        department = request.POST.get('department')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 1. Check for empty values
        if not all([student_id, name, department, email, password]):
            messages.error(request, 'All fields are mandatory.')
            return render(request, 'auth.html')

        # 2. JSON Validation (Authorized Students Only)
        try:
            with open('students_demo.json', 'r') as f:
                students_data = json.load(f)
                student_entry = next((s for s in students_data if s['student_id'] == student_id), None)

                if not student_entry:
                    messages.error(request, 'Student ID not recognized by University.')
                    return render(request, 'auth.html')
                
                if not student_entry.get('authorized', False):
                    messages.error(request, 'This Student ID is not authorized for EVON.')
                    return render(request, 'auth.html')
        except FileNotFoundError:
            messages.error(request, 'University Database not found.')
            return render(request, 'auth.html')

        # 3. Check for duplicates (Prevents the 1062 Error)
        if User.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID already in system. Please Sign In.')
            return render(request, 'auth.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'auth.html')

        # 4. Create User (Using create_user handles password hashing)
        user = User.objects.create_user(
            student_id=student_id,
            username=student_id, # Keep these synced
            name=name,
            department=department,
            email=email,
            password=password
        )
        login(request, user)
        return redirect('index')

    return render(request, 'auth.html')

def login_view(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')

        # authenticate looks for USERNAME_FIELD, which we set to student_id
        user = authenticate(request, username=student_id, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid Student ID or Key Phrase.")
            return render(request, 'auth.html')
            
    return render(request, 'auth.html')

def user_dashboard(request):
    if request.user.is_authenticated:
        payments = Payment.objects.filter(user=request.user)
        total_paid = payments.aggregate(Sum('amount'))['amount__sum'] or 0
        context = {
            'user': request.user,
            'payments': payments,
            'total_paid': total_paid,
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('login')

def index(request):
    return render(request, 'index.html')

@login_required
def payment_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        user = request.user

        Payment.objects.create(
            user=user,
            amount=amount,
            category=category
        )
        return redirect('index')
    # In case of a GET request, redirect to the home page or show an error
    return redirect('index')

def logout_view(request):
    logout(request)
    return redirect('index')

def get_remaining_time(user):
    try:
        booking = Booking.objects.filter(user=user).latest('start_time')
        plan = booking.plan
        duration = None

        if plan.duration_type == 'Hourly':
            duration = timedelta(hours=1)
        elif plan.duration_type == 'Daily':
            duration = timedelta(days=1)
        elif plan.duration_type == 'Weekly':
            duration = timedelta(weeks=1)
        elif plan.duration_type == 'Monthly':
            duration = timedelta(days=30)

        if duration:
            end_time = booking.start_time + duration
            remaining = end_time - timezone.now()

            if remaining.total_seconds() > 0:
                hours, remainder = divmod(remaining.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                return f"{hours}h {minutes}m"
            else:
                return "Expired"
        else:
            return "N/A"
    except Booking.DoesNotExist:
        return "No Bookings"

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('index')

    users = User.objects.filter(is_superuser=False)
    users_data = []

    for user in users:
        total_paid = Payment.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
        remaining_time = get_remaining_time(user) # Placeholder
        users_data.append({
            'user': user,
            'total_paid': total_paid,
            'remaining_time': remaining_time,
        })

    return render(request, 'admin_dashboard.html', {'users_data': users_data})
