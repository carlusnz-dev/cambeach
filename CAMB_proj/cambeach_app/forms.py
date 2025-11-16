from django import forms
from .models import Category, Tournament

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "genre")
        
class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('name', 'local', 'organization', 'start_date', 'end_date', 'n_players')