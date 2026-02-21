from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    student_id = models.CharField(max_length=20, unique=True, blank=False)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'student_id' 
    REQUIRED_FIELDS = ['username', 'name', 'department', 'email']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.student_id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.student_id

class RentalPlan(models.Model):
    title = models.CharField(max_length=100)
    duration_type = models.CharField(max_length=20, choices=[('Hourly', 'Hourly'), ('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly')])
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(RentalPlan, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    total_charge = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.user.student_id} - {self.plan.title}'

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.student_id} - {self.amount} - {self.category}'
