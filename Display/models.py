from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Perfil(models.Model):
    usuario=models.OneToOneField(User,on_delete=models.CASCADE)
    nome=models.CharField(max_length=30,blank=True,null=True)
    idade=models.IntegerField(null=True,blank=True,validators=[MaxValueValidator(100),MinValueValidator(10)])
    ftp=models.IntegerField(null=True,blank=True)
    peso=models.FloatField(null=True,blank=True)
    altura=models.FloatField(null=True,blank=True)

#Sinais para criação/atualização de Perfil em criação/atualização de Usuário
@receiver(post_save,sender=User)
def criar_perfil_usuario(sender,instance,created,**kwargs):
    if created:
        Perfil.objects.create(usuario=instance)
@receiver(post_save,sender=User)
def salvar_perfil_usuario(sender,instance,**kwargs):
    instance.perfil.save()
