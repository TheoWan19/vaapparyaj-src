from django.shortcuts import render, redirect
from django.contrib.auth import login

from .models import User
from .forms import CustomerSignUpForm, EmployeeSignUpForm

# Create your views here.
def customer_register(request):
	if request.user.is_authenticated:
		return redirect('home')

	if request.method == 'POST':
		form = CustomerSignUpForm(request.POST)
		if form.is_valid():
			user = form.save()	
			login(request, user)
			return redirect('home')
		else:
			for error in list(form.errors.values()):
				print(request, error)
	else:
		form = CustomerSignUpForm()
	return render(request=request, template_name='accounts/register.html', context={'form': form})	


def employee_register(request):

	if request.method == 'POST':
		form = EmployeeSignUpForm(request.POST)
		if form.is_valid():
			user = form.save()	
			login(request, user)
			return redirect('home')
		else:
			for error in list(form.errors.values()):
				print(request, error)
	else:
		form = EmployeeSignUpForm()
	return render(request=request, template_name='accounts/register.html', context={'form': form})	




def customer_home(request):
	context = {}
	return render(request, 'core/customer_home.html', context)		
