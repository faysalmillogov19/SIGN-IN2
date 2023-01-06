from django.db import models
from django.conf import settings

# Create your models here.
class Protocole(models.Model):
	nom=models.TextField()

class ServerConfiguration(models.Model):
	email = models.TextField()
	username= models.TextField(null=True)
	password= models.TextField()
	key= models.TextField()
	server_url= models.TextField(default="smtp.gmail.com")
	protocole=models.ForeignKey(Protocole, on_delete=models.CASCADE)
	port= models.IntegerField()

