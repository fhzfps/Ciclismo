from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models
#Formulário de Usuário:
class NovoUsuario(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        help_texts={'username':'<br><br><li>Digite um Nome de Usuário Alfanumérico.<li>150 caracteres ou menos.<br><br>'}
        labels={'username':'Nome de Usuário'}
    def __init__(self,*args,**kwargs):
        super(NovoUsuario, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text='''<br><br><li>Digite uma senha<li>Não pode conter informações similares às suas outras informações pessoais.
                       <li>No mínimo 8 caracteres.<br><br>'''
        self.fields['password1'].label='Senha'
        self.fields['password2'].help_text='<br><br><li>Confirme a senha digitada anteriormente.<br><br>'
        self.fields['password2'].label='Confirmação de Senha'
        self.fields['email'].help_text='<br><br><li>Digite um E-mail válido.<br><br>'
    def clean(self):
        cd=self.cleaned_data
        if User.objects.filter(email=cd.get('email')).exists():
            self.add_error('email','''
	        Email já cadastrado, registre-se utilizando outro e-mail.''')
        return cd
    def save(self, commit=True):
      user = super(NovoUsuario, self).save(commit=False)
      user.email = self.cleaned_data['email']
      if commit:
        user.save()
        return user

class NovoPerfil(forms.ModelForm):
    class Meta:
        model=models.Perfil
        fields=("nome","idade","ftp",'peso','altura')
        labels={'nome':'Nome:','idade':'Idade:','ftp':'FTP','peso':'Peso','altura':'Altura'}
    def save(self,commit=True):
        Perfil=super(NovoPerfil,self).save(commit=False)
        if commit:
            Perfil.save()
        return Perfil

class NovoTreino(forms.ModelForm):
    class Meta:
        model=models.Treino
        fields=('usuario',"tipo_arquivo","arquivo",'ftp','duracao_s','NP','IF','PM','TTS','CM','PMax',
                'PMin','CMax','CMin','Calorias','Distancia','GraficoPot','GraficoCad','GraficoZonas')
                
        labels={'tipo_arquivo':'Tipo do Arquivo:','arquivo':'Upload do Arquivo:'}
    def save(self,commit=True):
        Treino=super(NovoTreino,self).save(commit=False)
        if commit:
            Treino.save()
        return Treino
