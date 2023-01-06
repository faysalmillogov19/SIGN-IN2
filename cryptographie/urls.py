from django.contrib import admin
from django.urls import path,include,re_path
from . import views

urlpatterns = [
	
	path('add_personnal_signature',views.createPersonalSignatureImage,name="add_personnal_signature"),
	path('list_personnal_signature',views.ListPersonalSignatureImage,name="list_personnal_signature"),
	path('delete_personnal_signature/<int:id>',views.deletePersonalSignatureImage,name="delete_personnal_signature"),
	path('', views.index, name="crypter"),
	path('<str:link>', views.signataire_OTP_auth, name="signataire_OTP_auth"),
	path('form/<str:link>', views.other_signer_form, name="other_signers_form"),
	path('signer/<int:id>',views.other_signer,name="other_signers"),
    #re_path(r'^crypt/', views.crypter, name="crypter"),
]
