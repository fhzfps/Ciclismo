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

def user_dir(instance,filename):
    return f'user_{instance.usuario.id}/{filename}'

class Treino(models.Model):
    class FileTypes(models.TextChoices):
        TCX= '.tcx','.tcx'
    #Fornecido
    usuario=models.ForeignKey(User,on_delete=models.CASCADE,related_name='Treinos')
    tipo_arquivo=models.CharField(max_length=30,choices=FileTypes.choices,default=FileTypes.TCX)
    arquivo=models.FileField(upload_to=user_dir)
    #Calculado Posteriormente
    ftp=models.FloatField(null=True,blank=True)
    duracao_s=models.FloatField(null=True,blank=True)
    NP=models.FloatField(null=True,blank=True)
    IF=models.FloatField(null=True,blank=True)
    PM=models.FloatField(null=True,blank=True)
    TTS=models.FloatField(null=True,blank=True)
    CM=models.FloatField(null=True,blank=True)
    PMax=models.FloatField(null=True,blank=True)
    PMin=models.FloatField(null=True,blank=True)
    CMax=models.FloatField(null=True,blank=True)
    CMin=models.FloatField(null=True,blank=True)
    Calorias=models.FloatField(null=True,blank=True)
    Distancia=models.FloatField(null=True,blank=True)
    GraficoPot=models.TextField(null=True,blank=True)
    GraficoCad=models.TextField(null=True,blank=True)
    GraficoZonas=models.TextField(null=True,blank=True)

#Sinais para criação/atualização de Perfil em criação/atualização de Usuário
@receiver(post_save,sender=User)
def criar_perfil_usuario(sender,instance,created,**kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save,sender=User)
def salvar_perfil_usuario(sender,instance,**kwargs):
    instance.perfil.save()
