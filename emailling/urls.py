from django.contrib import admin
from django.urls import path,include,re_path
from . import views

urlpatterns = [
	path('', views.ServerconfigurationForm, name="email_server_configuration"),
    re_path(r'^set_email_configuration', views.setServerconfiguration, name="set_email_server_configuration"),
    #path('testemail', views.test, name="email_server_configuration_test"),
]
