from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('customer-register', views.customer_register, name='customer-register'),
    path('employee-register', views.employee_register, name='employee-register'),
    #path('login/', views.CustomLoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html',
    #                                       authentication_form=CustomAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('login', views.login_view, name='login'),
    path('verify/', views.verify_view, name='verify'),
    #path('logout', views.custom_logout, name='logout'),
    #path('login', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    #path('logout', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('password-change/', views.ChangePasswordView.as_view(), name='password_change'),
    path('activate/<uidb64>/<token>/', views.ActivationAccount.as_view(), name='activate'),
]