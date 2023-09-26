from django.shortcuts import render
from invoice.decorators import * 

# Create your views here.
def home(request):
	context={}
	return render(request, 'core/home.html', context)

@superuser_required
def employee_home(request):
	context={}
	return render(request, 'core/employee_home.html', context)	
