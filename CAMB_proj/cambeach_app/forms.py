from django import forms
from .models import Category, Tournament

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "genre")
        
# class CategoryChoiseField():
        
class TournamentForm(forms.ModelForm):
    start_date = forms.DateField(
        label="Data de início",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d', '%d/%m/%Y']
    )
    
    end_date = forms.DateField(
        label="Data de encerramento",
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d', '%d/%m/%Y']
    )
    
   # Meta 
    
    class Meta:
        model = Tournament
        fields = ('name', 'local', 'organization', 'start_date', 'end_date', 'n_players', 'categories')
        
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
        }