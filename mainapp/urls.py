from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [

	path('web-login', LoginView.as_view(), name = "web_login"),
	path('order', OrderView.as_view(), name = "order"),
	path('customers', CustomerView.as_view(), name = "customers"),
	path('search-address', SearchCustomer.as_view(), name = "search_address"),
	path('edit-customer', EditCustomer.as_view(), name = "edit_customer"),
	path('jobs', Jobs.as_view(), name = "jobs"),
	path('search-jobs>', SearchJobs.as_view(), name = "search_jobs"),
	path('edit-job>', EditJobLocation.as_view(), name = "edit_job"),


]
