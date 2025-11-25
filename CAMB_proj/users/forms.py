from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelChoiceField
from .models import Atleta
from cambeach_app.models import Category 

class CategoryChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} - {obj.get_genre_display()}"

class AtletaCreationForm(UserCreationForm):
    
    categoria_de_jogo = CategoryChoiceField(
        queryset=Category.objects.all(),
        label="Categoria de Jogo",
        empty_label="Selecione sua categoria de jogo",
        widget=forms.Select 
    )

    data_de_nascimento = forms.DateField(
        label="Data de Nascimento",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d', '%d/%m/%Y']
    )

    class Meta(UserCreationForm.Meta):
        model = Atleta
        fields = ('last_name', 'first_name', 'categoria_de_jogo', 'email', 'data_de_nascimento', 'telefone', 'cpf')