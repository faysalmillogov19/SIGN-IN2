from django.db import models

# Create your models here.
class Default_parameters(models.Model):
	url_2_base = models.TextField()
	port= models.TextField(null=True)
	signataire_url= models.TextField()
	OTP_time_validity= models.IntegerField()
	before_signature_alert_message_subject= models.TextField()
	before_signature_alert_message= models.TextField()
	signedFile_alert_sending_subject=models.TextField()
	signedFile_alert_sending_message=models.TextField()
	signature_certificat_objet=models.TextField(default="")
	signature_certificat_message=models.TextField(default="")
	signature_certificat_template_url=models.TextField(default="")

