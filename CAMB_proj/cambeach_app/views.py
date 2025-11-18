from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Tournament
from .forms import CategoryForm, TournamentForm
from django.db.models import Q

def inicio(request):
    categories = Category.objects.all()
    
    context = {
        'categories': categories
    }
    
    return render(request, 'inicio.html', context)

# Categorias
def category_form(request, pk=None):
    category = None
    
    if pk:
        category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = CategoryForm(instance=category)
        
    context = {'form': form, 'category': category}
    return render(request, 'category_form.html', context)

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    category.delete()
    return redirect('inicio')

# Tournament
@login_required
def tournament_form(request, pk=None):
    tournament = None
    
    if pk:
        tournament = get_object_or_404(Tournament, pk=pk)
    
    if request.method == 'POST':
        form = TournamentForm(request.POST, instance=tournament)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.user = request.user
            form.save()
            form.save_m2m()
            return redirect('tournament_create')
    else:
        form = TournamentForm(instance=tournament)
        
    context = {'form': form, 'tournament': tournament}
    return render(request, 'tournament_form.html', context)

# Tournement Views
def tornament(request):
    
    tournaments = Tournament.objects.all()
    query = request.GET.get('pesquisa')
    if query:
        tournaments = tournaments.filter(
            Q(name__icontains=query) |
            Q(local__icontains=query) |
            Q(organization__icontains=query)
        )
        
    context = {
        'tournaments': tournaments
    }
    
    return render(request, 'campeonatos.html', context)

def chaves(request):
    return render(request, 'chaves.html')

def organizador(request):
    return render(request, 'organizador.html')

def create_tournament_page(request):
    return render(request, 'criar_campeonato.html')
