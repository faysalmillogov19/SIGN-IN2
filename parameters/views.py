from django.shortcuts import render
from .models import Default_parameters

# Create your views here.

def default_parameters_form(request):
	config= Default_parameters.objects.first()
	return render(request,"default_parameters.html",{'config':config})

def add_default_parameters(request):
	if request.POST:
		param = Default_parameters()
		param.url_2_base = request.POST.get("url_2_base")
		param.port= request.POST.get("port")
		param.signataire_url= request.POST.get("signataire_url")
		param.OTP_time_validity= request.POST.get("OTP_time_validity")
		param.before_signature_alert_message_subject= request.POST.get("before_signature_alert_message_subject")
		param.before_signature_alert_message= request.POST.get("before_signature_alert_message")
		param.signedFile_alert_sending_subject= request.POST.get("signedFile_alert_sending_subject")
		param.signedFile_alert_sending_message= request.POST.get("signedFile_alert_sending_message")
		param.save()
	return render(request,"default_parameters.html",{'config':param})


def set_default_parameters(request):
	param= Default_parameters.objects.first()
	if request.POST:
		param.url_2_base = request.POST.get("url_2_base")
		param.port= request.POST.get("port")
		param.signataire_url= request.POST.get("signataire_url")
		param.OTP_time_validity= request.POST.get("OTP_time_validity")
		param.before_signature_alert_message_subject= request.POST.get("before_signature_alert_message_subject")
		param.before_signature_alert_message= request.POST.get("before_signature_alert_message")
		param.signedFile_alert_sending_subject= request.POST.get("signedFile_alert_sending_subject")
		param.signedFile_alert_sending_message= request.POST.get("signedFile_alert_sending_message")
		param.signature_certificat_objet= request.POST.get("signature_certificat_objet")
		param.signature_certificat_message= request.POST.get("signature_certificat_message")
		param.signature_certificat_template_url= request.POST.get("signature_certificat_template_url")
		param.save()
	return render(request,"default_parameters.html",{'config':param})	