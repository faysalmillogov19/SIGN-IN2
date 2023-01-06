from django.shortcuts import render


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from csrgenerator.models import  Cert
from cryptographie.models import Document,Signataire
from SIGN_IN import GlobalVar
import os

@login_required
def index(request):
	documents=Document.objects.filter(initiateur=request.user)
	print(documents)
	return render(request,"backend/listSignedDoc.html",{"documents":documents})

@login_required
def details_signed_doc(request, id):
	document=Document.objects.get(id=id)
	signataires=Signataire.objects.filter(document=document)
	return render(request,"backend/table.html",{"signataires":signataires})