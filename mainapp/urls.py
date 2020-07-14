from django.contrib import admin
from django.urls import path, include
from .views import *

from django.contrib.auth.decorators import login_required

urlpatterns = [
	path('', LoginView.as_view(), name = "login"),
	path('logout/', Logout.as_view(), name = "logout"),

	# URL related to customer process
	path('customers/', (CustomerView.as_view()), name = "customers"),
	path('search-address/', (SearchCustomer.as_view()), name = "search_address"),
	path('edit-customer/', (EditCustomer.as_view()), name = "edit_customer"),

	# URL related to job process
	path('jobs/', (Jobs.as_view()), name = "jobs"),
	path('search-jobs/', (SearchJobs.as_view()), name = "search_jobs"),
	path('edit-job/', (EditJobLocation.as_view()), name = "edit_job"),

	# URL related to order process
	path('order/', (OrderView.as_view()), name = "order"),

	path('order-search/', (OrderSearch.as_view()), name='order-search'),
	path('order-list/', (OrderListing.as_view()), name='order-list'),
	path('order-delete/', (OrderDelete.as_view()), name='order-delete')
	
]
