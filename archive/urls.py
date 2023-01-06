from django.contrib import admin
from django.urls import path,include,re_path
from . import views

urlpatterns = [
	path('', views.index, name="list_signed_document"),
    path('details/<int:id>', views.details_signed_doc, name="document_details"),
]
