from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Tournament, Team
from users.models import Atleta

class CategoryMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} - {obj.get_genre_display()}"

class CategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} - {obj.get_genre_display()}"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "genre")

class TeamForm(forms.ModelForm):
    cpf_parceiro = forms.CharField(label="CPF da Dupla", max_length=14)

    category = CategoryChoiceField(
        queryset=Category.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Categoria Disponivel",
        empty_label="Categoria Indisponivel",
    )

    class Meta:
        model = Team
        fields = ['category']

    def __init__(self, *args, **kwargs):
        self.tournament = kwargs.pop('tournament', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        
        if self.tournament:
            qs = self.tournament.categories.all()
            
            if self.user and self.user.categoria_de_jogo:
                qs = qs.filter(id=self.user.categoria_de_jogo.id)
            
            self.fields['category'].queryset = qs

    def clean(self):
        cleaned_data = super().clean()
        cpf_parceiro = cleaned_data.get('cpf_parceiro')
        parceiro = None

        try:
            parceiro = Atleta.objects.get(cpf=cpf_parceiro)
            cleaned_data['parceiro_obj'] = parceiro 
        except Atleta.DoesNotExist:
            raise ValidationError("CPF não encontrado.")

        if self.user and self.tournament:
            ja_inscrito = Team.objects.filter(
                tournament=self.tournament, 
                players=self.user
            ).exists()
            if ja_inscrito:
                raise ValidationError("Erro: VOCÊ já está inscrito em um time neste torneio.")

        if parceiro and self.tournament:
            parceiro_ja_inscrito = Team.objects.filter(
                tournament=self.tournament, 
                players=parceiro
            ).exists()
            if parceiro_ja_inscrito:
                raise ValidationError(f"Erro: O atleta {parceiro.first_name} já está inscrito neste torneio com outra dupla.")
        
        if parceiro == self.user:
             raise ValidationError("Você não pode formar dupla com você mesmo.")

        return cleaned_data

class TournamentForm(forms.ModelForm):
    categories = CategoryMultipleChoiceField(
        label="Categorias",
        widget=forms.CheckboxSelectMultiple,
        queryset=None 
    )
    name = forms.CharField(label="Nome do Campeonato", max_length=255)
    local = forms.CharField(label="Local", max_length=255)
    organization = forms.CharField(label="Organização", max_length=255)
    n_players = forms.IntegerField(label="Número de Participantes")
    start_date = forms.DateField(
        label="Data de Início",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        label="Data de Encerramento",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.all() 

    class Meta:
        model = Tournament
        fields = '__all__'