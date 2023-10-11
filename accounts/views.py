from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

from .models import User
from .forms import CustomerSignUpForm, EmployeeSignUpForm, CustomAuthenticationForm, UpdateUserForm, UpdateProfileForm

# Create your views here.
def customer_register(request):
	if request.user.is_authenticated:
		return redirect('/')

	if request.method == 'POST':
		form = CustomerSignUpForm(request.POST)
		if form.is_valid():
			user = form.save()	
			login(request, user)
			messages.success(request, f"New account created: {user.email}")
			return redirect('/')
		else:
			for error in list(form.errors.values()):
				messages.error(request, error)
	else:
		form = CustomerSignUpForm()
	return render(request=request, template_name='accounts/register.html', context={'form': form})	


def employee_register(request):

	if request.method == 'POST':
		form = EmployeeSignUpForm(request.POST)
		if form.is_valid():
			user = form.save()	
			login(request, user)
			messages.success(request, f"New account created: {user.email}")
			return redirect('/')
		else:
			for error in list(form.errors.values()):
				messages.error(request, error)
	else:
		form = EmployeeSignUpForm()
	return render(request=request, template_name='accounts/register.html', context={'form': form})	

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True
        	# else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py	
        return super(CustomLoginView, self).form_valid(form)


def customer_home(request):
	context = {}
	return render(request, 'core/customer_home.html', context)		

@login_required
def profile(request):
	if request.method == 'POST':
		user_form = UpdateUserForm(request.POST, instance=request.user)
		profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Your profile is updated successfully')
			return redirect(to='profile')
	else:
		user_form = UpdateUserForm(instance=request.user)
		profile_form = UpdateProfileForm(instance=request.user.profile)
	return render(request, 'accounts/profile.html', {'user_form': user_form, 'profile_form': profile_form})		

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
	template_name = 'accounts/change_password.html'
	success_message = "Successfully Changed Your Password"
	success_url = reverse_lazy('users-home')