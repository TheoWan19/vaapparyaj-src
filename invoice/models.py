from django.db import models
from django.utils.translation import gettext_lazy as _
import pytz
import uuid
from accounts.models import User, ClientUser

# Create your models here.


class Invoice(models.Model):
	INVOICE_TYPE = (
		('R', _('RECEIPT')),
		('I', _('INVOICE')),
	)

	invoice_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
	client = models.ForeignKey(ClientUser, on_delete=models.PROTECT)
	save_by = models.ForeignKey(User, on_delete=models.PROTECT)
	invoice_date_time = models.DateTimeField(auto_now_add=True)
	total = models.DecimalField(max_digits=1000, decimal_places=2)
	last_updated_date = models.DateTimeField(null=True, blank=True)
	paid = models.BooleanField(default=False)
	invoice_type = models.CharField(max_length=1, choices=INVOICE_TYPE)
	comments = models.TextField(null=True, max_length=1000, blank=True)

	class Meta:
		verbose_name = "Invoice"
		verbose_name_plural = "Invoices"

	def __str__(self):
		return f"{self.client.name}_{self.invoice_date_time}_{self.invoice_id}"	


	@property
	def get_total(self):
		articles = self.article_set.all()
		total = sum(article.get_total for article in articles)
		return total


class Article(models.Model):

	def odd_convert(self, odd=None):
		if odd:
			return int(self.odd)
		return None	

	id_bookmaker = models.IntegerField()
	bookmaker_name = models.CharField(max_length=255)
	id_bet = models.IntegerField()
	bet_name = models.CharField(max_length=255)
	value = models.IntegerField()
	odd = models.CharField(max_length=255)

	TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

	id_fixture = models.IntegerField()
	timezone = models.CharField(max_length=32, choices=TIMEZONES)
	timestamp= models.IntegerField()

	id_league = models.IntegerField()
	name = models.CharField(max_length=255)
	country = models.CharField(max_length=120)
	logo = models.URLField(max_length=200)	
	flag = models.URLField(max_length=200)
	season = models.IntegerField()

	quantity = models.IntegerField()
	unit_price = models.DecimalField(max_digits=1000, decimal_places=2, default=odd_convert(odd))	
	total = models.DecimalField(max_digits=1000, decimal_places=2)	


	class Meta:
		verbose_name = 'Article'
		verbose_name_plural = 'Articles'

	@property
	def get_total(self):
		total = self.quantity * self.unit_price
		return total