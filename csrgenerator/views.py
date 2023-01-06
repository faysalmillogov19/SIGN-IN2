from django.shortcuts import render
from OpenSSL import crypto 
from .models import Cert
import os, hashlib, sys
from datetime import datetime
from SIGN_IN import settings
import rsa
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import socket
import string,random
import cryptocode
from cryptographie.models import Signataire, Document
import os

@login_required
def index(request):
	key_size=[1024,2048, 4096]
	user=None
	if request.user.is_authenticated:
		user=User.objects.get(id=request.user.id)
		pays=Cert.objects.raw('SELECT * FROM pays')


	if request.POST:
		data = {
			'pays' :request.POST.get("pays"),
			'region' :request.POST.get("region"),
			'localite' :request.POST.get("localite"),
			'organisation' :request.POST.get("organisation"),
			'direction' :request.POST.get("direction"),
			'email' :request.POST.get("email"),
			'telephone' :request.POST.get("telephone"),
			'pass_phrase' :request.POST.get("pass_phrase"),
			'key_size' :request.POST.get("key_size"),
			'user' :user,
		}
		
		data=create_signed_cert(data,'static/uploads/csr/')
		result=save_cert(data)
		if(result):
			message="Votre certificat a bien ete enregistre"
		else:
			message="Un probleme est survenu lors de la creation du certificat"

		return render(request,'message.html',{'result':result, "message":message})
	else :
		
		return render(request,'createCsr.html',{'key_size':key_size,"pays":pays})

def createCertificat():
	return 0


def create_signed_cert(data,folder):


	cert_name= str(data['email'])+str(datetime.now().strftime("_%Y_%m_%d_%H_%M_%S"))+str('.pem')
	key_name= str(data['email'])+str(datetime.now().strftime("_%Y_%m_%d_%H_%M_%S"))+str('_key.pem')

	k = crypto.PKey()
	k.generate_key( crypto.TYPE_RSA, int(data['key_size']) )

	cert_req = crypto.X509Req()
	
	cert_req.get_subject().commonName = socket.gethostname()
	
	if data['pays'] :
		print(data['pays'])	
		cert_req.get_subject().C = data['pays']
	if data['region'] :
		cert_req.get_subject().ST = data['region']
	if data['localite'] :
		cert_req.get_subject().L = data['localite']
	if data['organisation'] :
		cert_req.get_subject().O = data['organisation']
	if data['email'] :
		cert_req.get_subject().emailAddress = data['email']
	if data['direction'] :
		cert_req.get_subject().OU = data['direction']
	if data['organisation'] :
		cert_req.get_subject().CN = data['organisation']

	#pass_phrase=hashlib.md5(data['pass_phrase'].encode()).hexdigest()
	
	cert_req.set_pubkey(k)
	cert_req.sign(k, 'sha256')

	cert_content=crypto.dump_certificate_request(crypto.FILETYPE_PEM, cert_req)
	#key_content=crypto.dump_privatekey(crypto.FILETYPE_PEM, k)

	cert_req.sign(k, 'sha256')
	cert = crypto.X509()
	cert.gmtime_adj_notBefore(0)
	cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
	cert.set_subject(cert_req.get_subject())
	cert.set_pubkey(cert_req.get_pubkey())
	cert.sign(k, 'sha256')

	cert_content=crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
	pass_phrase=data['pass_phrase'].encode()
	key_content=crypto.dump_privatekey(crypto.FILETYPE_PEM, k, passphrase=pass_phrase )

	open(folder+cert_name, "x").write(  cert_content.decode('UTF-8') )
	open(folder+key_name,  "x").write(   key_content.decode('UTF-8') )

	data['nom_cert']= cert_name #hashlib.md5(cert_name.encode()).hexdigest()	
	data['nom_key']= key_name #hashlib.md5(key_name.encode()).hexdigest()
	#data['pass_phrase']=pass_phrase
	
	return data


def save_cert(data):

	privkey = get_random_string(20)
	cert = Cert()
	cert.pays =data["pays"]
	cert.region =data["region"]
	cert.localite =data["localite"]
	cert.organisation =data["organisation"]
	cert.direction =data["direction"]
	cert.email =data["email"]
	cert.telephone =data["telephone"]
	cert.pass_phrase =cryptocode.encrypt(data["pass_phrase"],   privkey)
	cert.key_size =data["key_size"]
	cert.nom_cert= cryptocode.encrypt("static/uploads/csr/"+data['nom_cert'], privkey)
	cert.nom_key = cryptocode.encrypt("static/uploads/csr/"+data['nom_key'],  privkey)
	cert.decrypt=privkey
	if(data["user"]):
		cert.user=data["user"]
	
	cert.save()

	return True

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

@login_required
def liste_certificat(request):
	certificats= Cert.objects.filter(user=request.user)
	return render(request,'backend/liste_certificats.html',{"certificats":certificats})

@login_required
def delete(request, id):
	cert=Cert.objects.get(id=id)
	doc_exist=Document.objects.filter(cert=cert)
	signataires_exit=Signataire.objects.filter(cert=cert)
	if(doc_exist or signataires_exit):
		return 0
	else:
		os.remove(cryptocode.decrypt(cert.nom_key,     password=cert.decrypt))
		os.remove(cryptocode.decrypt(cert.nom_cert,     password=cert.decrypt))
		cert.delete()
		return liste_certificat(request)	