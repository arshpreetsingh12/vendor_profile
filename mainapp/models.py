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


class Order(models.Model):
	""" This table for store Job Location. """
	customer = models.ForeignKey(Customerinformation, on_delete=models.CASCADE)
	labor = models.CharField(max_length=200,null = True, blank = True)
	labor_price = models.FloatField(default = 0.0)
	floor_prep = models.CharField(max_length=200, null = True, blank = True)
	floor_prep_price = models.FloatField(default = 0.0)
	sub_floor = models.CharField(max_length=200, null = True, blank = True)
	sub_floor_price = models.FloatField(default = 0.0)
	appliances = models.CharField(max_length=200, null = True, blank = True)
	appliances_price = models.FloatField(default = 0.0)
	miscellaneous = models.CharField(max_length=200, null = True, blank = True)
	miscellaneous_price = models.FloatField(default = 0.0)
	price_includes = models.CharField(max_length=200, null = True, blank = True)
	price_includes_price = models.FloatField(default = 0.0)
	sub_total = models.FloatField(default = 0.0)
	sales_tax = models.CharField(max_length=200,null = True, blank = True)
	total = models.FloatField(default = 0.0)
	deposit = models.FloatField(default = 0.0)
	balance_due = models.FloatField(default = 0.0)

	# def __str__(self):
	# 	return self.customer

class Products(models.Model):
	""" This table for store Job Location. """
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null = True)
	product_name = models.CharField(max_length=200)
	color = models.CharField(max_length=200, null = True, blank = True)
	qty = models.CharField(max_length=200, null = True, blank = True)
	area = models.CharField(max_length=500, null = True, blank = True)
	price = models.FloatField()
	

	# def __str__(self):
	# 	return self.customer

class Notes(models.Model):
	""" This table for store Job Location. """
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null = True)
	customer_notes = models.TextField(max_length=500, null = True, blank = True)
	job_site_notes = models.TextField(max_length=500, null = True, blank = True)


class Terms(models.Model):
	""" This table for store Job Location. """
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null = True)
	terms = models.TextField(max_length=500, null = True, blank = True)
