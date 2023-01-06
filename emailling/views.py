from django.shortcuts import render
from django.http import HttpResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.message import EmailMessage
from .models import ServerConfiguration, Protocole
from csrgenerator.views import get_random_string
import cryptocode, ssl
from parameters.models import Default_parameters


def ServerconfigurationForm(request):
	protocoles=Protocole.objects.all()
	config=ServerConfiguration.objects.first()
	return render(request, 'Email_Server_Configuration.html',{"protocoles":protocoles,'config':config})

def setServerconfiguration(request):
	if request.POST:
		config= config=ServerConfiguration.objects.get(id=int(request.POST.get("id")))
		config.email=request.POST.get("email")
		config.username=request.POST.get("username")
		config.key=get_random_string(20)
		config.password=cryptocode.encrypt(request.POST.get("password"), config.key)
		config.server_url=request.POST.get("server_url")
		config.protocole=Protocole.objects.get(id=int( request.POST.get("protocole") ) ) 
		config.port=request.POST.get("port")
		config.save()
	return ServerconfigurationForm(request)


# Create your views here.
def Send_mailFile(subject, message, destinataire, filename):
	try:
		config= ServerConfiguration.objects.first()
		monMail=config.email
		monPassword=cryptocode.decrypt(config.password, config.key)
		smtpserver=config.server_url
		port=config.port
		server=smtplib.SMTP(smtpserver,port)
		server.ehlo()
		server.starttls()
		server.login(monMail,monPassword)
		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject		#f"Subject: {subject}\n{message}"
		msg['From'] = monMail
		msg['To'] = destinataire
		msg.attach(MIMEText(message.encode('utf-8'), _charset='utf-8'))		
		part = MIMEBase('application', 'octate-stream')
		part.set_payload(open(filename, 'rb').read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename='+filename)
		msg.attach(part)
		#server.sendmail(monMail,destinataire,msg.as_string())
		server.sendmail(monMail,destinataire,msg.as_string())
		i= 1
	except:
		i= 0
	return i

def Send_mailText(subject, message, toaddr):
	config= ServerConfiguration.objects.first()
	monMail=config.email
	monPassword=cryptocode.decrypt(config.password, config.key)
	smtp_server=config.server_url
	port=config.port

	i=0
	context = ssl.create_default_context()
	try:
		server = smtplib.SMTP(smtp_server,port)
		server.starttls(context=context)
		server.login(monMail, monPassword)
		msg = MIMEText(message.encode('utf-8'), _charset='utf-8')
		msg['Subject'] = subject	#f"Subject: {subject}\n{message}"
		msg['From'] = monMail
		msg['To'] = toaddr
		server.sendmail(monMail, toaddr, msg.as_string())
		i=1
	except Exception as exep:
		i=0
	finally:
		server.quit()
	return 1

def default_parameters_values():
	parameters=Default_parameters.objects.first()
	if not "https://" in parameters.url_2_base and not "http://" in parameters.url_2_base:
		parameters.url_2_base="https://"+parameters.url_2_base

	if parameters.port:
		parameters.url_2_base=parameters.url_2_base+"/:"+parameters.port+"/"

	parameters.signataire_url=parameters.signataire_url.replace("/","")+"/"

	return parameters

def test(request):
	#r=Send_mailFile('Soumission du fichier', 'Hello bonjour tout le monde !!!!!', 'milfay19@gmail.com',"static/test.pdf")
	msg=default_parameters_values()
	subject=msg.before_signature_alert_message_subject
	url=msg.url_2_base+msg.signataire_url
	message=msg.before_signature_alert_message+"\n"+url
	r=Send_mailText(subject, message, 'milfay19@gmail.com')
	return HttpResponse(r)
