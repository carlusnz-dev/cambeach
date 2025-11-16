from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Atleta

class AtletaCreationForm(UserCreationForm):
    data_de_nascimento = forms.DateField(
        label="Data de Nascimento",
        required=False, # Seu modelo permite blank=True
        # Isso diz ao navegador para mostrar um calendário
        widget=forms.DateInput(attrs={'type': 'date'}), 
        input_formats=['%Y-%m-%d', '%d/%m/%Y'] # Aceita os dois formatos
    )
    class Meta(UserCreationForm.Meta):
        model = Atleta
        # Escolha os campos que o usuário deve preencher no cadastro
        fields = ('last_name', 'first_name' , 'genero' , 'categoria' , 'email' ,  'data_de_nascimento', 'telefone' , 'cpf')
        
        widgets = {
            'genero': forms.RadioSelect,
            'categoria': forms.RadioSelect,
        }