from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customerinformation(models.Model):
	""" This table for store Customer details. """
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	company = models.CharField(max_length=200)
	biling_address = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	postal_code = models.CharField(max_length=200)
	home_phone = models.CharField(max_length=200, null = True, blank = True)
	business_phone = models.CharField(max_length=200)
	fax_number = models.CharField(max_length=200, null = True, blank = True)
	cell_phone = models.CharField(max_length=200, null = True, blank = True)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.first_name

class JobLocation(models.Model):
	""" This table for store Job Location. """
	customer = models.OneToOneField(Customerinformation, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200, null = True, blank = True)
	phone_number = models.CharField(max_length=200, null = True, blank = True)
	address = models.TextField(max_length=500, null = True, blank = True)
	state = models.CharField(max_length=200)
	city = models.CharField(max_length=200, null = True, blank = True)
	postal_code = models.CharField(max_length=200, null = True, blank = True)
	

	# def __str__(self):
	# 	return self.customer