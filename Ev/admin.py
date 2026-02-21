from django.contrib import admin
from .models import User, RentalPlan, Booking

admin.site.register(User)
admin.site.register(RentalPlan)
admin.site.register(Booking)
