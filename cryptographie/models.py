from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from csrgenerator.models import  Cert
# Create your models here.

class Document(models.Model):
	nom = models.TextField()
	organisation = models.CharField(max_length=255)
	initiateur= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	cert=models.ForeignKey(Cert, on_delete=models.CASCADE)
	nombre_signataire=models.IntegerField(default=1)
	image = models.TextField(default="")
	ttf=models.TextField(default="")
	signed=models.BooleanField(default=False)
	file_hash=models.TextField(default="")
	created_at =models.DateTimeField(auto_now_add=True)

class Signataire(models.Model):
	document = models.ForeignKey(Document, on_delete=models.CASCADE,default=1)
	email = models.EmailField(max_length=255)
	nom_complet = models.TextField(max_length=255)
	telephone=models.TextField()
	image=models.TextField()
	ttf=models.TextField()
	link=models.TextField(default="")
	ordre=models.IntegerField(default=1)
	cert=models.ForeignKey(Cert, on_delete=models.CASCADE,null=True,blank=True)
	signed=models.BooleanField(default=False)
	file_hash=models.TextField(default="")
	signed_date =models.DateTimeField(auto_now=True, auto_now_add=False)

class Personal_Signature_Image(models.Model):
	user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	image_data=models.TextField(null=True)
	image_url=models.TextField(null=True)
	created_at =models.DateTimeField(auto_now_add=True)