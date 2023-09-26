from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


from .models import User

class RegistrationForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = ('email', 'name', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'location', 'password')
		widgets = {
			'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
			'phone': PhoneNumberPrefixWidget(initial='US'),
		}

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user
		
		
class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'name', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'location', 'is_active','is_staff', 'is_superuser')

		def clean_password2(self):
			password1 = self.cleaned_data.get('password1')
			password2 = self.cleaned_data.get('password2')	
			if password1 and password2 and password1 != password2:
				raise forms.ValidationError("Password don't match")
			return password2
			
		def save(self, commit=True):
			user = super().save(commit=False)
			user.set_password(self.cleaned_data['password1'])
			if commit:
				user.save()
			return user
			
class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('email', 'name', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'location', 'password', 'is_active', 'is_staff', 'is_superuser')	

	def clean_password(self):
		return self.initial['password']	


class CustomerSignUpForm(UserCreationForm):

	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	email = forms.EmailField(widget=forms.EmailInput())
	name = forms.CharField(widget=forms.TextInput())
	phone = PhoneNumberField()
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
	password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput())

	first_name = forms.CharField(widget=forms.TextInput())
	last_name = forms.CharField(widget=forms.TextInput())
	date_of_birth = forms.DateField()
	gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES)
	location = forms.CharField(widget=forms.TextInput())
		

	class Meta:
		model = User
		fields = ['email', 'name', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'location', 'password1', 'password2']
		widgets = {
			'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
			'phone': PhoneNumberPrefixWidget(initial='US'),
		}

	
	def save(self, commit=True):
		user = super(CustomerSignUpForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.is_customer = True
		if commit:
			user.save()

		return user
		

class EmployeeSignUpForm(UserCreationForm):

	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	email = forms.EmailField(widget=forms.EmailInput())
	name = forms.CharField(widget=forms.TextInput())
	phone = PhoneNumberField()
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
	password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput())

	first_name = forms.CharField(widget=forms.TextInput())
	last_name = forms.CharField(widget=forms.TextInput())
	date_of_birth = forms.DateField()
	gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES)
	location = forms.CharField(widget=forms.TextInput())
		

	class Meta:
		model = User
		fields = ['email', 'name', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'location', 'password1', 'password2']
		widgets = {
			'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
			'phone': PhoneNumberPrefixWidget(initial='US'),
		}

	
	def save(self, commit=True):
		user = super(EmployeeSignUpForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.is_employee = True
		if commit:
			user.save()

		return user		