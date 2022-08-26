from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns=[path('',views.home,name='home'),
             path('accounts/register',views.register,name='register'),
             path('accounts/perfil',views.perfil,name='perfil'),
             path('accounts/perfil/alt_perfil',views.perfil_form,name='alt_perfil'),
             path('accounts/perfil/novo_treino',views.treino_form,name='novo_treino'),
             path('accounts/perfil/editar_treinos',views.editar_treinos,name='editar_treinos'),
             path('accounts/perfil/editar_treinos/deletar/<int:id>',views.deletar_treino,name='deletar_treino'),
             path('accounts/perfil/visualizacao_treino',views.visualizar_treino,name='visualizar_treino'),
]
