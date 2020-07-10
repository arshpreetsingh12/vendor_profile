#imports
from django.views.generic import View
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect,HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.urls import reverse
from .models import *
import json

""" 
	This view for user login  
								"""
class LoginView(View):
	template_name = "login.html"

	def get(self,request):
		return render(request,self.template_name,locals())

	def post(self, request, *args, **kwargs):
		email = request.POST.get('email')
		password = request.POST.get('password')
		try:
			if email != "" and password != "": 
				user= User.objects.get(Q(email = email)|Q(username = email))

				if user.is_active == True:
					userauth = authenticate(username=user.username, password=password)
					if userauth:
						login(request, user,backend='django.contrib.auth.backends.ModelBackend')	
						return HttpResponseRedirect(reverse('order'))
							
					else:
						messages.error(request,'Invalid credentials.')
						return HttpResponseRedirect(reverse('web_login'))
			else:
				messages.error(request,'Incorrect email and password.')
				return HttpResponseRedirect(reverse('web_login'))

		except Exception as e:
			print(str(e))
			messages.info(request,'No such account exist.')
			return HttpResponseRedirect(reverse('web_login'))


class CustomerView(View):
	template_name = "customer.html"

	def get(self,request):

		return render(request,self.template_name,locals())

	def post(self, request):

		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		company = request.POST.get('company')
		billing_address = request.POST.get('billing_address')
		city = request.POST.get('city')
		state = request.POST.get('state')
		post_code = request.POST.get('post_code')
		home_phone = request.POST.get('home_phone')
		business_phone = request.POST.get('business_phone')
		fax_number = request.POST.get('fax_number')
		cell_phone = request.POST.get('cell_phone')
		email = request.POST.get('email')

		try:
			user = User.objects.get(email = email)
			messages.info(request,"User already exist with given email.")
			return HttpResponseRedirect(reverse('customers'))

		except User.DoesNotExist:
			user = User.objects.create(
				username = email, 
				email = email,
				first_name = first_name,
				last_name = last_name,
			)
			add_customer = Customerinformation.objects.create(
					user = user,
					company = company,
					biling_address = billing_address,
					city = city,
					state = state,
					postal_code = post_code,
					home_phone = home_phone,
					business_phone = business_phone,
					fax_number = fax_number,
					cell_phone = cell_phone
				)
			messages.success(request,"Customer successfilly added.")
			return HttpResponseRedirect('/jobs/'+ str(add_customer.id))
		except Exception as e:
			messages.error(request,"Something went wrong.")
			return HttpResponseRedirect(reverse('customers'))
	


class SearchCustomer(View):
	def post(self, request):
		response = {}
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		search_cell_phone = request.POST.get('cell_phone')
		found_user = ""

		if last_name and email:
			found_user = Customerinformation.objects.filter(user__email = email, user__last_name = last_name).last()

		if last_name and email and search_cell_phone:
			found_user = Customerinformation.objects.filter(user__email = email, user__last_name = last_name, cell_phone = search_cell_phone).last()

		if found_user:
			response['status'] = True
			response['user_id'] = found_user.user.id
			response['email'] = found_user.user.email
			response['first_name'] = found_user.user.first_name
			response['last_name'] = found_user.user.last_name
			response['email'] = found_user.user.email
			response['company'] = found_user.company
			response['biling_address'] = found_user.biling_address
			response['city'] = found_user.city
			response['state'] = found_user.state
			response['postal_code'] = found_user.postal_code
			response['home_phone'] = found_user.home_phone
			response['business_phone'] = found_user.business_phone
			response['fax_number'] = found_user.fax_number
			response['cell_phone'] = found_user.cell_phone
		else:
			response['status'] = False
			response['msg'] = "No user found"

		return HttpResponse(json.dumps(response), content_type = 'application/json')


class EditCustomer(View):
	def post(self, request):
		user_id = request.POST.get('user_id')
		first_name = request.POST.get('edit_fisrt_name')
		last_name = request.POST.get('edit_last_name')
		company = request.POST.get('edit_company')
		billing_address = request.POST.get('edit_billing_address')
		city = request.POST.get('edit_city')
		state = request.POST.get('edit_state')
		post_code = request.POST.get('edit_postal_code')
		home_phone = request.POST.get('edit_home_phone')
		business_phone = request.POST.get('edit_business_phone')
		fax_number = request.POST.get('edit_fax_number')
		cell_phone = request.POST.get('edit_cell_phone')
		email = request.POST.get('edit_email')

		try:
			user = User.objects.get(id = user_id)
			user.first_name = first_name
			user.last_name = last_name
			user.email = email
			user.save()
			add_customer = Customerinformation.objects.filter(
					user = user).update(
					company = company,
					biling_address = billing_address,
					city = city,
					state = state,
					postal_code = post_code,
					home_phone = home_phone,
					business_phone = business_phone,
					fax_number = fax_number,
					cell_phone = cell_phone
				)
			messages.success(request,"User successfilly updated.")
			return HttpResponseRedirect(reverse('customers'))
		except Exception as e:
			print(e)
			messages.error(request,"Something went wrong.Please try again.")
			return HttpResponseRedirect(reverse('customers'))

class Jobs(View):
	template_name = "jobs.html"

	def get(self,request,customer_id):
	
		try:
			customer = Customerinformation.objects.get(pk = str(customer_id))
		except Customerinformation.DoesNotExist:
			messages.error(request,"Customer does not exist.")
		return render(request,self.template_name,locals())

	def post(self, request,customer_id):

		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		phone_number = request.POST.get('phone_number')
		address = request.POST.get('address')
		city = request.POST.get('city')
		state = request.POST.get('state')
		post_code = request.POST.get('post_code')
		
		try:
			customer = Customerinformation.objects.filter(pk = str(customer_id)).last()
			if customer:
				job_obj = JobLocation.objects.get(customer = customer)
				messages.info(request,"Job location already exist for this customer.")
			else:
				messages.error(request,"Invalid customer.")	
			return HttpResponseRedirect('/jobs/'+ str(customer_id))
		except JobLocation.DoesNotExist:
			customer = Customerinformation.objects.filter(pk = str(customer_id)).last()
			add_job = JobLocation.objects.create(
					customer = customer,
					first_name = first_name,
					last_name = last_name,
					phone_number = phone_number,
					address = address,
					state = state,
					city = city,
					postal_code = post_code
				)
			messages.success(request,"Job location successfilly added.")
			return HttpResponseRedirect(reverse('order'))

class SearchJobs(View):
	def post(self, request):
		response = {}
		last_name = request.POST.get('last_name')
		searchd_contact_number = request.POST.get('search_contact_number')
		searchd_city = request.POST.get('search_city')
		searchd_zip = request.POST.get('search_zip')
		found_job = ""

		if last_name and searchd_contact_number:
			found_job = JobLocation.objects.filter(last_name = last_name, phone_number = searchd_contact_number).last()

		if last_name and searchd_contact_number and searchd_city:
			found_job = JobLocation.objects.filter(last_name = last_name, phone_number = searchd_contact_number, city = searchd_city).last()

		if last_name and searchd_contact_number and searchd_zip:
			found_job = JobLocation.objects.filter(last_name = last_name, phone_number = searchd_contact_number, postal_code = searchd_zip).last()	
		
		if last_name and searchd_contact_number and searchd_city and searchd_zip:
			found_job = JobLocation.objects.filter(last_name = last_name, phone_number = searchd_contact_number, city = searchd_city, postal_code = searchd_zip).last()

		if found_job:
			response['status'] = True
			response['job_id'] = found_job.id
			response['first_name'] = found_job.first_name
			response['last_name'] = found_job.last_name
			response['phone_number'] = found_job.phone_number
			response['address'] = found_job.address
			response['state'] = found_job.state
			response['city'] = found_job.city
			response['postal_code'] = found_job.postal_code
		else:
			response['status'] = False
			response['msg'] = "No job found"

		return HttpResponse(json.dumps(response), content_type = 'application/json')



class OrderView(View):
	template_name = "order.html"

	def get(self,request):
		return render(request,self.template_name,locals())


class EditJobLocation(View):
	def post(self, request):
		job_id = request.POST.get('job_id')
		first_name = request.POST.get('edit_fisrt_name')
		last_name = request.POST.get('edit_last_name')
		address = request.POST.get('edit_address')
		city = request.POST.get('edit_city')
		state = request.POST.get('edit_state')
		edit_postal_code = request.POST.get('edit_postal_code')

		try:
			job_obj = JobLocation.objects.get(pk = job_id)
			job_obj.first_name = first_name
			job_obj.last_name = last_name
			job_obj.address = address
			job_obj.state = state
			job_obj.city = city
			job_obj.postal_code = edit_postal_code
			job_obj.save()
		
			messages.success(request,"Job location successfully updated.")
			return HttpResponseRedirect(reverse('order'))
		except Exception as e:
			print(e)
			messages.error(request,"Something went wrong.Please try again.")
			return HttpResponseRedirect('/jobs/'+ str(job_id))