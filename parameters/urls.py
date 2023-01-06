from django.contrib import admin
from django.urls import path,include,re_path
from . import views

urlpatterns = [
	#path('', views.index, name="log_in"),
    path('', views.default_parameters_form, name="default_parameters"),
    re_path(r'^set_default_parameters', views.set_default_parameters, name="set_default_parameters"),
]
