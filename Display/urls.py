from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns=[path('',views.home,name='home'),
             path('accounts/register',views.register,name='register'),
             path('accounts/perfil',views.perfil,name='perfil'),
             path('accounts/perfil/alt_perfil',views.perfil_form,name='alt_perfil'),
]
