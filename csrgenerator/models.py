from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Cert(models.Model):
	pays = models.CharField(max_length=255)
	region = models.CharField(max_length=255, null=True)
	localite= models.CharField(max_length=255, null=True)
	organisation = models.CharField(max_length=255)
	user= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
    )
	direction = models.CharField(max_length=255, null=True)
	email = models.EmailField()
	telephone= models.CharField(max_length=255)
	pass_phrase = models.TextField()
	key_size = models.IntegerField()
	nom_cert = models.TextField()
	nom_key = models.TextField()
	decrypt = models.CharField(max_length=255, null=True)
	created_at =models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(null=True)
