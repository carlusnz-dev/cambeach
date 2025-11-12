from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Atleta

class AtletaCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Atleta
        # Escolha os campos que o usuário deve preencher no cadastro
        fields = ('nome_completo', 'email', 'genero', 'categoria', 'idade', 'telefone' , 'cpf')
        