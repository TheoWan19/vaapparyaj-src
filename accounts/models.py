from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
#from django.db.models.signals import post_save
#from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


import os
from . managers import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
	def image_upload_to(self, instance=None):
		if instance:
			return os.path.join("Users", self.email, instance)
		return None	

	user_type_data=((1,"User"),(2,"ClientUser"))
	user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)


	email = models.EmailField(unique=True)
	phone = PhoneNumberField(unique=True)
	first_name = models.CharField(max_length=120)
	last_name = models.CharField(max_length=120)
	date_of_birth = models.DateField(blank=True, null=True)
	gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name='Gender')
	is_staff = models.BooleanField(default=False)
	is_customer = models.BooleanField(default=True)
	is_employee = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)
	date_joined = models.DateTimeField(default=timezone.now)
	modified_at = models.DateTimeField(auto_now=True)
	last_login = models.DateTimeField(null=True)
	location = models.CharField(max_length=500)



	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['phone', ]


	def get_full_name(self):
		return f'{self.first_name }'+' '+ f'{self.last_name}'.title()

	def get_short_name(self):
		return self.email.split()[0]	


class ClientUser(models.Model):

	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	email = models.EmailField(unique=True)
	phone = PhoneNumberField(unique=True)
	first_name = models.CharField(max_length=120)
	last_name = models.CharField(max_length=120)
	gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name='Gender')
	location = models.CharField(max_length=255)
	city = models.CharField(max_length=100)
	address = models.CharField(max_length=255)
	zip_code = models.CharField(max_length=100)
	age = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	modifed_at = models.DateTimeField(auto_now=True)
	save_by = models.ForeignKey(User, on_delete=models.PROTECT)
	


	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []


	def get_full_name(self):
		return f'{self.first_name }'+' '+ f'{self.last_name}'.title()

	def get_short_name(self):
		return self.email.split()[0]

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
	cin = models.CharField(max_length=10)
	nif = models.CharField(max_length=10)
	designation = models.CharField(max_length=100)
	bio = models.TextField()

	date_modified = models.DateTimeField(User, auto_now=True)

	def __str__(self):
		return self.user.email

def save(self, *args, **kwargs):
    super().save()

    img = Image.open(self.avatar.path)

    if img.height > 100 or img.width > 100:
        new_img = (100, 100)
        img.thumbnail(new_img)
        img.save(self.avatar.path)