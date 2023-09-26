from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, name, phone, password, **extra_fields):
		values = [email, name, phone]
		fields_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
		for field_name, value in fields_value_map.items():
			if not value:
				raise ValueError('The {} value must bet set'.format(field_name))

		email = self.normalize_email(email)
		user = self.model(
			email=email,
			name=name,
			phone=phone,
			**extra_fields
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, name, phone, password=None, **extra_fields):	
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', False)	
		return self._create_user(email, name, phone, password, **extra_fields)		

	def create_superuser(self, email, name, phone, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, name, phone, password, **extra_fields)			