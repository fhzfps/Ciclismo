from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.forms import UserCreationForm
from . import models
from . import forms
from .BikeUtils import BikeAnalyze
from django.core.files.base import ContentFile
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

@login_required
def perfil(request):
    template=loader.get_template('perfil.html')
    return HttpResponse(template.render(request=request))

@login_required
def perfil_form(request):
    template=loader.get_template('registration/perfil_form.html')
    if request.method=='POST':
        form=forms.NovoPerfil(request.POST)
        if form.is_valid():
            request.user.perfil.nome=request.POST['nome']
            request.user.perfil.ftp=request.POST['ftp']
            request.user.perfil.peso=request.POST['peso']
            request.user.perfil.altura=request.POST['altura']
            request.user.perfil.idade=request.POST['idade']
            request.user.perfil.save()
            return HttpResponseRedirect('/accounts/perfil')
        else:
            return HttpResponse(template.render(context={'register_form':form},request=request))
    form=forms.NovoPerfil()
    context={'register_form':form}
    return HttpResponse(template.render(context=context,request=request))

@login_required
def treino_form(request):
    template=loader.get_template('registration/treino_form.html')
    if request.method=='POST':
        form=forms.NovoTreino(request.POST,request.FILES)
        if form.is_valid():
            treino=form.save(commit=False)
            relatorio=BikeAnalyze(file=treino.arquivo,file_type=treino.tipo_arquivo,ftp=request.user.perfil.ftp).gerar_relatorio()
            #try:
            treino.usuario=request.user
            treino.ftp=request.user.perfil.ftp
            treino.duracao_s=relatorio['duracao_s']
            treino.NP=relatorio['NP']
            treino.IF=relatorio['IF']
            treino.PM=relatorio['PM']
            treino.TTS=relatorio['TTS']
            treino.CM=relatorio['CM']
            treino.PMax=relatorio['PMax']
            treino.PMin=relatorio['PMin']
            treino.CMax=relatorio['CMax']
            treino.CMin=relatorio['CMin']
            treino.Calorias=relatorio['Calorias']
            treino.Distancia=relatorio['Distancia']
            temp_file_pot=ContentFile(relatorio['GraficoPot'].encode('utf-8'))
            treino.GraficoPot.save(f'pot_{treino.id}.html',temp_file_pot)
            temp_file_cad=ContentFile(relatorio['GraficoCad'].encode('utf-8'))
            treino.GraficoCad.save(f'cad_{treino.id}.html',temp_file_cad)
            temp_file_zonas=ContentFile(relatorio['GraficoZonas'].encode('utf-8'))
            treino.GraficoZonas.save(f'zonas_{treino.id}.html',temp_file_zonas)
            treino.save()
            #except:
                #return HttpResponse(loader.get_template('erro_analise.html').render(request=request))
            return HttpResponseRedirect('/accounts/perfil')
        else:
            return HttpResponse(template.render(context={'register_form':form},request=request))
    form=forms.NovoTreino()
    context={'register_form':form}
    return HttpResponse(template.render(context=context,request=request))

@login_required
def editar_treinos(request):
    template=loader.get_template('treinos.html')
    treino_lst=request.user.Treinos.all()
    context={'treino_data':treino_lst}
    return HttpResponse(template.render(context=context,request=request))

@login_required
def deletar_treino(request,id):
    treino=request.user.Treinos.filter(id=id)
    treino.delete()
    return HttpResponseRedirect('/accounts/perfil/editar_treinos')


@login_required
def visualizar_treino(request):
    template=loader.get_template('registration/meus_treinos_form.html')
    if request.method=='POST':
        treino=request.user.Treinos.get(id=int(request.POST['Treinos']))
        return HttpResponse(loader.get_template('visualizar_treino.html').render(request=request,context={'treino':treino}))
    user_treinos=request.user.Treinos.all()
    return HttpResponse(template.render(request=request,context={'user_treinos':user_treinos}))
