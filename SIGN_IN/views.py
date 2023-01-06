from django.shortcuts import  render, redirect, reverse
from django.http import JsonResponse
from os import listdir
from os.path import isfile, join
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from csrgenerator.models import Cert
import time,os
from datetime import datetime
from django.core.files.storage import default_storage
import uuid
from cryptographie.models import Personal_Signature_Image
from cryptographie.SignModules import create_own_signatureImage


@login_required
def home(request):
    return render(request, "registration/success.html", {})
 
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            file=request.FILES["image"]
            extension=File[1]
            print('###############')
            print(extension)
            name=uploadFile(file, "static/uploads/files/Signature_sample_images/default", extension)
            img= Personal_Signature_Image()
            img.image_url= name
            img.save()
            #user = authenticate(username = username, password = password)
            #login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def index(request):
	return render(request, 'index.html')

def liste_membres(request):
	return render(request, 'membres.html')
	
@login_required
def sign_form(request):
	
	list_signataires=[]
	if request.session.get('signataires'):
		list_signataires=request.session.get('signataires')
	return render(request, 'sign_form.html',{'liste_signataires':list_signataires})


@login_required
def add_PDF_doc(request):
	if request.POST:
		certificats= Cert.objects.filter(user=request.user)
		return render(request, 'sign_form_add_FichierPDF.html',{"certificats":certificats})


@login_required
def add_SIGNATURE_pdf(request):
	if request.POST :
		cert=request.POST.get("cert")

		personal_signatures=Personal_Signature_Image.objects.filter(user=request.user)

		file=request.FILES['document']
		name = file.name
		file_name='static/uploads/files/tamp/'+name
		ts = str(time.time())+"pdf"
		own_signature_name=str(datetime.now().strftime("_%Y_%m_%d_%H_%M_%S"))+str('.png')
		own_signature_name='static/uploads/Signature_sample_images/custom_signature/tamp'+own_signature_name
	
		if not os.path.exists(file_name):
			default_storage.save('static/uploads/files/tamp/'+name, file)		

		default_signatures_images_folder='static/uploads/Signature_sample_images/' 
		default_signatures_images = [default_signatures_images_folder+f for f in listdir(default_signatures_images_folder) if isfile(join(default_signatures_images_folder, f))]

		return render(request, 'signed_form_add_Signature.html',{'default_signatures_images':default_signatures_images,'default_signatures_images_folder':default_signatures_images_folder,"cert":cert,"file_name":file_name, 'own_signature_name':own_signature_name,'personal_signatures':personal_signatures})


def add_new_signataire(request):
	id=0
	if request.POST:
		signataire={
			'email': request.POST.get('email'),
			'nom_complet': request.POST.get('nom_complet'),
			'telephone': request.POST.get('telephone'),
			'id':request.POST.get('id'),
		}
		if request.session.get('signataires'):
			if request.POST.get('id'):
				set_signataire(request)
			else:
				new_signataire(request,signataire)
		else:
			list=[]
			signataire['id']=1;
			list.append(signataire)
			request.session['signataires']=list

		id=signataire['id']
				
	return redirect('/sign')
	#render(request, 'sign_form.html',{'liste_signataires':request.session.get('signataires'),'id':id})
	#return JsonResponse({'list_signataire': request.session.get('signataires'),'id':id})
def new_signataire(request,signataire):
	list=request.session.get('signataires')
	signataire['id']=max(d['id'] for d in list)+1
	list.append(signataire)
	request.session['signataires']=list
			
def set_signataire(request):
	seted=False
	if request.POST:
		
		if request.session.get('signataires'):
			id=request.POST.get('id')
			list=request.session.get('signataires')
			
			for i in range(len( list )):
				if int(list[i]['id'])==int(id):
					list[i]['nom_complet']=request.POST.get('nom_complet')
					list[i]['email']=request.POST.get('email')
					list[i]['telephone']=request.POST.get('telephone')
					break
								
			request.session['signataires']=list
	return JsonResponse({'response': seted})

	

def delete_signataire(request):
	deleted=False
	if request.POST:
		
		if request.session.get('signataires'):
			id=request.POST.get('id')
			list=request.session.get('signataires')
			
			for i in range(len( list )):
				if int(list[i]['id'])==int(id):
					del list[i]
					deleted=True
					break
								
			request.session['signataires']=list
	return JsonResponse({'response': deleted})


			
def destroy_signataire(request):
	if request.session.get('signataires'):
		del request.session['signataires']
	return JsonResponse({'response':True}) 