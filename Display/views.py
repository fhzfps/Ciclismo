from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import UserCreationForm
from . import models
from . import forms

#Teste se usuário possui permissão completa
def supuser(user):
    return user.is_superuser

#Página Inicial
def home(request):
    template=loader.get_template('homepage.html')
    return HttpResponse(template.render(request=request))

#Registro de Novo Usuário
def register(request):
    template= loader.get_template('registration/register.html')
    if request.method == "POST":
        form = forms.NovoUsuario(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponse(template.render(context={'register_form':form},request=request))
    form = forms.NovoUsuario()
    context={"register_form":form}
    return HttpResponse(template.render(context,request))
