from django.contrib import admin
from django.urls import path, include
from .views import *

from django.contrib.auth.decorators import login_required

urlpatterns = [
	path('', LoginView.as_view(), name = "login"),
	path('logout/', Logout.as_view(), name = "logout"),
	path('web-login/', LoginView.as_view(), name = "web_login"),

	# URL related to customer process
	path('customers/', login_required(CustomerView.as_view()), name = "customers"),
	path('search-address/', login_required(SearchCustomer.as_view()), name = "search_address"),
	path('edit-customer/', login_required(EditCustomer.as_view()), name = "edit_customer"),

	# URL related to job process
	path('jobs/', login_required(Jobs.as_view()), name = "jobs"),
	path('search-jobs>/', login_required(SearchJobs.as_view()), name = "search_jobs"),
	path('edit-job/', login_required(EditJobLocation.as_view()), name = "edit_job"),

	# URL related to order process
	path('order/', login_required(OrderView.as_view()), name = "order"),
	path('add-customer-notes/', login_required(AddCustomerNotes.as_view()), name = "add_customer_notes"),
	path('add-terms/', login_required(AddTerms.as_view()), name = "add_terms"),

	path('order-search/', login_required(OrderSearch.as_view()), name='order-search')
	
]
