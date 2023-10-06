from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('customer-register', views.customer_register, name='customer-register'),
    path('employee-register', views.employee_register, name='employee-register'),
    path('login', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
]