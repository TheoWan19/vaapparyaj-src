from django.urls import path
from . import views

urlpatterns = [
    path('customer-register', views.customer_register, name='customer-register'),
    path('employee-register', views.employee_register, name='employee-register'),
]