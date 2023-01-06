from django.conf.urls import url
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse
from django.core.files.storage import default_storage
from Crypto.Cipher import AES
from PyPDF2 import PdfFileWriter, PdfFileReader
import random
import time
from pyhanko import stamp
from pyhanko.pdf_utils import text, images
from pyhanko.pdf_utils.font import opentype
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers,fields
from . import SignModules

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Document,Signataire,Personal_Signature_Image
from csrgenerator.models import  Cert
from csrgenerator.views import save_cert, create_signed_cert
from emailling import views
from SIGN_IN import GlobalVar
import cryptocode
import os
import base64
from datetime import datetime
from PIL import Image
from io import BytesIO
import string,random,uuid

from emailling.views import Send_mailText, Send_mailFile
import pyotp
import hashlib
from parameters.models import Default_parameters


# Create your views here.
def get_random_link(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return cryptocode.crypt( result_str, password=str( datetime.now().strftime("_%Y_%m_%d_%H_%M_%S") ) )

def default_parameters_values():
	parameters=Default_parameters.objects.first()
	if not "https://" in parameters.url_2_base and not "http://" in parameters.url_2_base:
		parameters.url_2_base="http://"+parameters.url_2_base

	if parameters.port:
		parameters.url_2_base=parameters.url_2_base+":"+parameters.port+"/"

	parameters.signataire_url=parameters.signataire_url.replace("/","")+"/"

	return parameters

@login_required
def index(request):

	signataires=[]
	if request.POST:
		cert=Cert.objects.get(id=int(request.POST.get("cert")))
		im_signed=bool(int(request.POST.get("im_signed")))
		img=request.POST.get('default_image')
		image_for_signin=img
		own_signature=bool(int(request.POST.get("own_signature")))
		key= cryptocode.decrypt(cert.nom_key,     password=cert.decrypt)
		crt= cryptocode.decrypt(cert.nom_cert,    password=cert.decrypt)
		mdp= cryptocode.decrypt(cert.pass_phrase, password=cert.decrypt) #cert.pass_phrase.encode() #''#b'P@ssw0rd123' 
		position=(200, 600, 300, 300)
		ttf='static/uploads/ttf-samples/OpenSans-Bold.ttf'
		msg=default_parameters_values()
		url=msg.url_2_base+msg.signataire_url
		nom_complet=request.user.username
		file_name=request.POST.get("file_name")
		
		
		doc = Document()
		doc.initiateur=request.user
		doc.cert=cert
		doc.organisation=cert.organisation
		doc.signed=im_signed
		doc.file_hash=hash_file(file_name)

		if im_signed:
			if own_signature:
				image_for_signin=SignModules.create_own_signatureImage(img)
			doc.ttf=ttf
			doc.image=img
			doc.nom=SignModules.signature(crt, key, file_name, mdp.encode(), nom_complet, image_for_signin, position, ttf, url)
			os.remove(file_name)
		else:
			doc.nom=file_name

		if own_signature:
			os.remove(image_for_signin)

		doc.save() 
		i=0
		j=0
		if request.session.get('signataires'):
			list_signataire=request.session.get('signataires')
			for i in range(len( list_signataire )):
					j=+1
					
					signatair= Signataire()
					signatair.document=doc
					signatair.email=list_signataire[i]['email']
					signatair.nom_complet=list_signataire[i]['nom_complet']
					signatair.telephone=list_signataire[i]['telephone']
					signatair.ordre=i
					signatair.link=uuid.uuid4()
					if(i==0):
						msg=default_parameters_values()
						subject=msg.before_signature_alert_message_subject
						url=msg.url_2_base+msg.signataire_url+str(signatair.link)
						message=msg.before_signature_alert_message+'\n'+url
						t=Send_mailText(subject, message, signatair.email)
						print(t)
					
					signatair.save()
			i=j
			del request.session['signataires']
			doc.nombre_signataire=j
			doc.save()
		
	doc.nom_complet=request.user.username
	return render(request, 'signed_message.html',{'signataire':doc})

def  genarate_key(longer):
	key=""
	for i in range(longer):
		key+=str(random.randint(0, 9))
	return key

def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()


def signataire_OTP_auth(request, link):
	totp = pyotp.TOTP('base32secret3232')
	if request.POST:
		otp=str(request.POST.get('otp'))
		
		if request.session.get("code_otp")==otp:
			request.session['signataire']="OTP"
			del request.session['code_otp']
			return redirect(other_signer_form, link=link)
	else:
		if request.session.get('signataire'):
			del request.session['signataire']
		signatair=Signataire.objects.filter(link=link).first()
		code=totp.now()
		request.session['code_otp']=code
		#print(type(code))
		t=Send_mailText("Code OTP SIGN-IN","Le code :"+code, signatair.email)
		#time.sleep(30)
	return render(request, "signataire_OTP_Auth.html",{'link':link})

def other_signer_form(request, link):
	if request.session.get('signataire'):	

		signatair=Signataire.objects.filter(link=link).first()
		if signatair.signed:
			signatair.document.nom=signatair.document.nom.replace('static/', '')
			signatair.image=signatair.image.replace('static/', '')
			return render(request, 'signed_message.html',{'signataire':signatair})
			
		else:
			var=GlobalVar.GlobalVar()
			file=signatair.document.nom.replace('static/', '')

			cert_exit= Cert.objects.filter(email=signatair.email).first()
			document=Document.objects.get(id=signatair.document.id)

			if cert_exit:
				key= cryptocode.decrypt(cert_exit.nom_key,     password=cert_exit.decrypt)
				crt= cryptocode.decrypt(cert_exit.nom_cert,     password=cert_exit.decrypt)
				mdp= cryptocode.decrypt(cert_exit.pass_phrase,     password=cert_exit.decrypt)
			else:
				data = {
					'pays' :'',
					'region' :'',
					'localite' :'',
					'organisation' :'',
					'direction' :'',
					'email' :signatair.email,
					'telephone' :signatair.telephone,
					'pass_phrase' :'',
					'key_size' :1024,
					'user' :'',
				}
				data=create_signed_cert(data,'static/uploads/csr/')
				save_cert(data)

		certificats= Cert.objects.filter(email=signatair.email)

		return render(request, 'other_signers.html', {'signataire':signatair,'default_signatures_images':var.get_default_images(),'file':file,"certificats":certificats} )
	else:
		return redirect(signataire_OTP_auth, link=link)


def other_signer(request, id):
	if request.session.get('signataire'):

		signatair=Signataire.objects.get(id=id)
		if request.POST:
			cert_exit= Cert.objects.filter(email=signatair.email).first()
			document=Document.objects.get(id=signatair.document.id)


			key= cryptocode.decrypt(cert_exit.nom_key,     password=cert_exit.decrypt)
			crt= cryptocode.decrypt(cert_exit.nom_cert,     password=cert_exit.decrypt)
			mdp= cryptocode.decrypt(cert_exit.pass_phrase,     password=cert_exit.decrypt)
			own_signature=bool(int(request.POST.get("own_signature")))
			
			image_for_signin=request.POST.get('default_image') 
			signatair.image=image_for_signin 
			 
			position=(200, 200, 400, 600)
			signatair.ttf='static/uploads/ttf-samples/OpenSans-Bold.ttf'

			file_name=document.nom
			signatair.file_hash=hash_file(file_name)

			if own_signature:
				image_for_signin=SignModules.create_own_signatureImage(signatair.image)

			document.nom=SignModules.signature(crt, key, file_name, mdp, signatair.nom_complet, image_for_signin, position, signatair.ttf, GlobalVar.GlobalVar().signed_url)
			document.save()
			os.remove(file_name)
			signatair.signed=True
			signatair.save()

		signatair.document.nom=signatair.document.nom.replace('static/', '')
		signatair.image=signatair.image.replace('static/', '')
		get_next_signataire(signatair.id, signatair.document.id)
		var=[signatair.document.file_hash, signatair.nom_complet, signatair.email, signatair.telephone, signatair.email]
		certificat_signature=SignModules.add_text_to_PDF(var, image_for_signin, "output_file_name.pdf")
		msg=default_parameters_values()
		subject=msg.before_signature_alert_message_subject
		message=str(msg.before_signature_alert_message)
		t=views.Send_mailFile(subject, message, signatair.email, certificat_signature)
		os.remove(certificat_signature)
		return render(request, 'signed_message.html',{'signataire':signatair})


def get_next_signataire(signatair_id, document_id):
	signatair= Signataire.objects.filter(id=signatair_id+1).first()

	if not signatair:
		get_all_signataires(document_id)
	elif signatair.document.id==document_id :
		msg=default_parameters_values()
		subject=msg.before_signature_alert_message_subject
		url=msg.url_2_base+msg.signataire_url+str(signatair.link)
		message=str(msg.before_signature_alert_message+url)
		t=Send_mailText(subject, message, signatair.email)
	else:
		get_all_signataires(document_id)
	

def get_all_signataires(document_id):
	signataires= Signataire.objects.filter(document=document_id)	

	for signatair in signataires:
		msg=default_parameters_values()
		subject=msg.signedFile_alert_sending_subject 
		message=msg.signedFile_alert_sending_message
		t=views.Send_mailFile(subject, message, signatair.email, signatair.document.nom)		


def createPersonalSignatureImage(request):
	if request.POST:
		image= Personal_Signature_Image()
		image.user=request.user
		image.image=request.POST.get("default_signature")
		image.save()
		return HttpResponse(image.image)
	
	return HttpResponse({'response','Erreur'})

@login_required
def ListPersonalSignatureImage(request):
	images=Personal_Signature_Image.objects.filter(user=request.user)

@login_required
def deletePersonalSignatureImage(request,id):
	image=Personal_Signature_Image.objects.get(id=id)
	image.delete()

