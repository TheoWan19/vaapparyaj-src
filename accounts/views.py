from typing import Protocol
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.views import LoginView
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .models import User
from .forms import CustomerSignUpForm, EmployeeSignUpForm, CustomAuthenticationForm, UpdateUserForm, UpdateProfileForm
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from invoice.decorators import * 

# Create your views here.

@user_not_authenticated
def customer_register(request):
	if request.method == 'POST':
		form = CustomerSignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)	
			user.is_activate = False
			user.save()

			current_site = get_current_site(request)
			mail_subject = 'Activate Your Vaapparyaj Account'
			message = render_to_string('accounts/account_activation_email.html', {
										'user': user,
										'domain': current_site.domain,
										'uid': urlsafe_base64_encode(force_bytes(user.pk)),
										'token': account_activation_token.make_token(user),
			})
			to_email = form.cleaned_data.get('email')

			email = EmailMessage(
				mail_subject, message, to=[to_email]
			)

			email.send()
			messages.success(request, ('Please Confirm your email to complete registration.'))
			return redirect('login')
		else:
			for error in list(form.errors.values()):
				messages.error(request, error)
	else:
		form = CustomerSignUpForm()
	return render(request=request, template_name='accounts/register.html', context={'form': form})


@superuser_required
@employee_required
def employee_register(request):
	if request.method == 'POST':
		form = EmployeeSignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)	
			user.is_activate = False
			user.save()

			current_site = get_current_site(request)
			mail_subject = 'Activate Your Vaapparyaj Account'
			message = render_to_string('accounts/account_activation_email.html', {
										'user': user,
										'domain': current_site.domain,
										'uid': urlsafe_base64_encode(force_bytes(user.pk)),
										'token': account_activation_token.make_token(user),
			})
			to_email = form.cleaned_data.get('email')

			email = EmailMessage(
				mail_subject, message, to=[to_email]
			)

			email.send()
			messages.success(request, ('Please Confirm your email to complete registration.'))
			return redirect('login')
		else:
			for error in list(form.errors.values()):
				messages.error(request, error)
	else:
		form = EmployeeSignUpForm()
	return render(request=request, template_name='accounts/register.html', context={'form': form})


class ActivationAccount(View):

	def get(self, request, uidb64, token, *args, **kwargs):
		try:
			uid = force_str(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
		except (TypError, ValueError, OverFlowError, User.DoesNotExist):
			user = None

		if user is not None and account_activation_token.check_token(user, token):
			user.is_active = True
			user.save()
			login(request, user)
			messages.success(request, ('Your account have been confirmed.'))
			return redirect('login')
		else:
			messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
			return redirect('home')


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