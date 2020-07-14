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
import time
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.db import transaction
""" 
	This view for user login  
								"""
class LoginView(View):
	template_name = "login.html"

	def get(self,request):

		if request.user.is_authenticated and request.user.is_active:
			return HttpResponseRedirect(reverse('customers'))
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
						return HttpResponseRedirect(reverse('customers'))
							
					else:
						messages.error(request,'Invalid credentials.')
						return HttpResponseRedirect(reverse('login'))
			else:
				messages.error(request,'Incorrect email and password.')
				return HttpResponseRedirect(reverse('login'))

		except Exception as e:
			print(str(e))
			messages.info(request,'No such account exist.')
			return HttpResponseRedirect(reverse('login'))

""" 
	This view for user logout  
								"""
class Logout(View):

	def post(self, request, *args, **kwargs):
		print('\n'*5)
		print('inside logout post')
		logout(request)
		return HttpResponseRedirect(reverse('login'))


class CustomerView(LoginRequiredMixin,View):
	login_url = '/'
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
			request.session['customer_id'] = add_customer.id
			messages.success(request,"Customer successfilly added.")
			return HttpResponseRedirect(reverse('jobs'))
		except Exception as e:
			messages.error(request,"Something went wrong.")
			return HttpResponseRedirect(reverse('customers'))
	


class SearchCustomer(LoginRequiredMixin,View):
	login_url = '/'

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


class EditCustomer(LoginRequiredMixin, View):
	login_url = '/'

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

class Jobs(LoginRequiredMixin,View):
	login_url = '/'
	template_name = "jobs.html"

	def get(self,request):
		customer_id = request.session.get('customer_id')
		return render(request,self.template_name,locals())

	def post(self, request):
		response = {}
		customer_id = request.POST.get('customer_id')
		first_name = request.POST.get('fisrt_name')
		last_name = request.POST.get('last_name')
		phone_number = request.POST.get('phone_number')
		address = request.POST.get('address')
		city = request.POST.get('city')
		state = request.POST.get('state')
		post_code = request.POST.get('post_code')

		try:
			if customer_id != 'None':
				customer = Customerinformation.objects.filter(pk = str(customer_id)).last()
				if customer:
					job_obj = JobLocation.objects.get(customer = customer)
					# messages.info(request,"Job location already exist for this customer.")
					response['status'] = False
					response['msg'] = "Job location already exist for this customer."
				else:
					response['status'] = False
					response['msg'] = "Please add new customer first."
					# messages.error(request,"Please add new customer first.")
			else:
				response['status'] = False
				response['msg'] = "Please add new customer first."
				# messages.error(request,"Please add new customer first.")	
			# return HttpResponseRedirect(reverse('jobs'))
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
			response['customer_id'] = customer.id
			response['status'] = True
			# response['msg'] = "Please add new customer first."
			# messages.success(request,"Job location successfilly added.")
		return HttpResponse(json.dumps(response), content_type = 'application/json')

class SearchJobs(LoginRequiredMixin, View):
	login_url = '/'

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

class EditJobLocation(LoginRequiredMixin, View):
	login_url = '/'

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
			return HttpResponseRedirect('/jobs')


class OrderView(LoginRequiredMixin,View):
	template_name = "order.html"
	login_url = '/'

	def get(self,request):
		return render(request,self.template_name,locals())

	def post(Self, request):
		response = {}
		products = json.loads(request.POST.get('product_data'))
		labor_dis = request.POST.get('labor_dis')
		labor_price = request.POST.get('labor_price')
		floor_des = request.POST.get('floor_des')
		floor_price = request.POST.get('floor_price')
		sub_floor_des = request.POST.get('sub_floor_des')
		sub_floor_price = request.POST.get('sub_floor_price')
		appliances = request.POST.get('appliances')
		appliances_price = request.POST.get('appliances_price')
		trim = request.POST.get('trim')
		trim_price = request.POST.get('trim_price')
		miscellaneous_des = request.POST.get('miscellaneous_des')
		miscellaneous_price = request.POST.get('miscellaneous_price')
		price_include = request.POST.get('price_include')
		price_include_price = request.POST.get('price_include_price')
		sub_tot = request.POST.get('sub_tot')
		total_amount = request.POST.get('total_amount')
		deposite_amount = request.POST.get('deposite_amount')
		due_balance = request.POST.get('due_balance')
		sale_tax = request.POST.get('sale_tax')
		customer_id = request.session.get('customer_id')
		terms = request.POST.get('terms')
		customer_notes = request.POST.get('customer_notes')
		job_site_notes = request.POST.get('job_site_notes')

		time_obj = time.time()
		change_time_obj = int(time_obj)

		try:
			with transaction.atomic():
				add_order = Order.objects.create(
					customer_id = customer_id
					# customer_id = 1,
					)
				if labor_dis:
					add_order.labor = labor_dis
				if labor_price:
					add_order.labor_price = labor_price
				if floor_des:
					add_order.floor_prep = floor_des
				if floor_price:	
					add_order.floor_prep_price = floor_price
				if sub_floor_des:
					add_order.sub_floor = sub_floor_des
				if sub_floor_price:
					add_order.sub_floor_price = sub_floor_price
				if appliances:
					add_order.appliances = appliances
				if appliances_price:
					add_order.appliances_price = appliances_price
				if miscellaneous_des:
					add_order.miscellaneous = miscellaneous_des
				if miscellaneous_price:
					add_order.miscellaneous_price = miscellaneous_price
				if price_include:
					add_order.price_includes = price_include
				if price_include_price:
					add_order.price_includes_price = price_include_price
				if sub_tot:
					add_order.sub_total = sub_tot
				if sale_tax:
					add_order.sales_tax = sale_tax
				if total_amount:
					add_order.total = total_amount
				if deposite_amount:
					add_order.deposit = deposite_amount
				if due_balance:
					add_order.balance_due = due_balance
				if trim:
					add_order.trim = trim
				if trim_price:
					add_order.trim_price = trim_price
				add_order.order_id = change_time_obj + int(add_order.id)
				add_order.is_deleted = False
				add_order.save()

				for data in products:
					add_product = Products.objects.create(
						order = add_order,
						product_name = data['product_service'],
						color = data['color'],
						qty = data['qty'],
						area = data['area'],
						price = data['product_price']
						
					)

				Terms.objects.create(
					order = add_order,
					terms = terms
				)

				Notes.objects.create(
					customer_notes = customer_notes,
					 job_site_notes = job_site_notes,
					 order = add_order
				)

				html_string2 = render_to_string('order-invoice-pdf.html',  locals())
				html = HTML(string=html_string2, base_url=request.build_absolute_uri(),)
				html.write_pdf(target= settings.BASE_DIR + '/media/invoices/'+ str(add_order.order_id) + '.pdf');
				invoice_file = 'invoices/' + str(add_order.order_id) + '.pdf'
				seller_email = [add_order.customer.user.email]
				email_from = settings.EMAIL_HOST_USER
				subject ="Order Invoice"
				message = ""
				msgs = EmailMessage(subject ,message  , email_from, seller_email )
				msgs.content_subtype = "html" 
				msgs.attach_file(settings.BASE_DIR + '/media/' + invoice_file)
				msgs.send()
				add_order.invoice_file = invoice_file
				add_order.save()
				response['msg'] = "Order successfully submit"
				response['status'] = True
			
		except Exception as e:
			raise e
			response['status'] = False
		return HttpResponse(json.dumps(response), content_type = 'application/json')


class OrderSearch(LoginRequiredMixin, View):
	template_name = "modify-order.html"
	login_url = '/'

	def get(self,request):
		return render(request,self.template_name)

	def post(self, request, *args, **kwargs):
		response = {}
		last_name = request.POST.get('last_name')
		order_id = request.POST.get('order_id')
		order_intake = request.POST.get('order_intake')
		found_order = ""

		try:
			if last_name and order_id:
				found_order = Order.objects.filter(order_id = order_id, 
					customer__user__last_name = last_name).last()

			if last_name and order_id and order_intake:
				found_order = Order.objects.filter(order_id = order_id, 
					customer__user__last_name = last_name).last()

			if found_order:
				response['first_name'] = found_order.customer.user.first_name
				response['order_id'] = order_id
				response['email'] = found_order.customer.user.email
				response['msg'] = "Order successfully found."
				response['status'] = True
			else:
				response['msg'] = "Order not found with given information."
				response['status'] = False
		except Exception as e:
			response['msg'] = "Something went wrong."
			response['status'] = False

		return HttpResponse(json.dumps(response), content_type = 'application/json')

class OrderListing(LoginRequiredMixin, View):
	template_name = "order-listing.html"
	login_url = '/'

	def get(self,request):
		orders = Order.objects.filter(is_deleted = False)
		return render(request,self.template_name,locals())

class OrderDelete(View):

	def post(self,request):
		response = {}
		order_id = request.POST.get('delete_order_id')
		try:
			order = Order.objects.get(pk = order_id)
			order.is_deleted = True
			order.save()
			response['msg'] = "Order successfully deleted."
			response['status'] = True
		except Exception as e:
			print(e)
			response['msg'] = "Something went wrong.Please try again."
			response['status'] = False
		return HttpResponse(json.dumps(response), content_type = 'application/json')
		
