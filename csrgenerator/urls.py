from django.contrib import admin
from django.urls import path,include,re_path
from . import views

urlpatterns = [
	path('', views.index, name="add_csr"),
	path('list_cert', views.liste_certificat, name="liste_certificat"),
	path('delete/<int:id>', views.delete, name="delete_cert"),
    #re_path(r'^add', views.create, name="add_user"),
]
