from django.contrib import admin
from django.urls import path,include,re_path
from . import views

urlpatterns = [
	#path('', views.index, name="log_in"),
    re_path(r'^add', views.create, name="add_user"),
    #re_path(r'^logout', views.deconnexion, name="log_out"),
]
