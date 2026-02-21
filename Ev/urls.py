from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('pay/', views.payment_view, name='payment'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
