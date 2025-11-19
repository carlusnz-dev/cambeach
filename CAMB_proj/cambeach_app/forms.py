from django import forms
from .models import Category, Tournament

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "genre")
        
# class CategoryChoiseField():
        
class TournamentForm(forms.ModelForm):
    # Campos CharField/IntegerField (Definidos explicitamente para segurança)
    categories = forms.ModelMultipleChoiceField(
        label="Categorias",
        widget=forms.CheckboxSelectMultiple,
        queryset=None # Deixamos None aqui
    )

    # 2. Definimos os outros campos explicitamente (como você já tinha)
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

    # 3. Movemos a consulta do banco para o __init__
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # A consulta só é feita AGORA, quando o formulário é instanciado na View.
        self.fields['categories'].queryset = Category.objects.all()

    class Meta:
        model = Tournament
        fields = '__all__'