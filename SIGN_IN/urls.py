"""SIGN_IN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', views.register, name='register' ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
	path('', views.index, name="accueil"),
    #re_path(r'^mylogin/', include('manageuser.urls'),),
    re_path(r'^csr/',include('csrgenerator.urls'),),
    re_path(r'^archive/',include('archive.urls'),),
    re_path(r'^sign/', views.sign_form, name="sign"),
    path('add_pdf_doc', views.add_PDF_doc, name="add_pdf_doc"),
    path('add_signature_pdf', views.add_SIGNATURE_pdf, name="add_signature_pdf"),
    re_path(r'^signer/', views.add_new_signataire, name="signer"),
    re_path(r'^delete_signer/', views.delete_signataire, name="delete_signer"),
    re_path(r'^destroy_signer/', views.destroy_signataire, name="destroy_signer"),
    re_path(r'^sign_in/', include('cryptographie.urls'), ),
	re_path(r'^membres/', views.liste_membres, name="membres"),
    path('admin/', admin.site.urls),
    re_path(r'^emailling/', include('emailling.urls'), ),
    re_path(r'^parameters/', include('parameters.urls'), ),
    path('accounts/', include('django.contrib.auth.urls'))
]
