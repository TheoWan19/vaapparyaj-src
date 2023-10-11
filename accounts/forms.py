from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField, AuthenticationForm
from django.contrib.auth.models import Group
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.forms.widgets import DateInput


from .models import User, Profile

class RegistrationForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = ('email', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'location', 'password')
		widgets = {
			'date_of_birth': DateInput(attrs={'type': 'date'}),
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
		fields = ('email', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'location', 'is_active','is_staff', 'is_superuser', 'password1')

		def clean_password2(self):
			password1 = self.cleaned_data.get('password1')
			password2 = self.cleaned_data.get('password2')	
			if password1 and password2 and password1 != password2:
				raise forms.ValidationError("Password don't match")
			return password2
			
		def save(self, commit=True):
			user = super().save(commit=False)
			user.set_password(self.cleaned_data['password'])
			if commit:
				user.save()
			return user
			
class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('email', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'location', 'password', 'is_active', 'is_staff', 'is_superuser')	

	def clean_password(self):
		return self.initial['password']	


class CustomerSignUpForm(forms.ModelForm):

	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = ('email', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'location', 'password1', 'password2')
		widgets = {
			'date_of_birth': DateInput(attrs={'type': 'date'}),
			'phone': PhoneNumberPrefixWidget(initial='US'),
		}

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		user.is_customer = True
		if commit:
			user.save()
		return user
		

class EmployeeSignUpForm(forms.ModelForm):

	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = ('email', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender', 'location', 'password1', 'password2')
		widgets = {
			'date_of_birth': DateInput(attrs={'type': 'date'}),
			'phone': PhoneNumberPrefixWidget(initial='US'),
		}

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		user.is_employee = True
		if commit:
			user.save()
		return user


class CustomAuthenticationForm(AuthenticationForm):
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'remember_me']

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = PhoneNumberField()

    class Meta:
        model = User
        fields = ['email', 'phone', 'date_of_birth']
        widgets = {
			'date_of_birth': DateInput(attrs={'type': 'date'}),
			'phone': PhoneNumberPrefixWidget(initial='US'),
		}


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    nif = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cin = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    designation = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'nif', 'cin', 'designation', 'bio']