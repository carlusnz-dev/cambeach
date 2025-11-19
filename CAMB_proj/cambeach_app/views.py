from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Tournament, Team, Match
from .forms import CategoryForm, TournamentForm
from django.db.models import Q
from random import shuffle

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

def chaves(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    matches = Match.objects.filter(tournament=tournament).order_by('category_of_match', 'id')
    
    context = {
        'tournament': tournament,
        'matches': matches
    }
    
    return render(request, 'chaves.html', context)

def gerar_chaves(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    
    for category in tournament.categories.all():
        teams = list(Team.objects.filter(tournament=tournament, category=category))
        shuffle(teams)
        
        for i in range(0, len(teams), 5):
            grupo_atual = teams[i : i + 5]
            
            for idx_a in range(len(grupo_atual)):
                for idx_b in range(idx_a + 1, len(grupo_atual)):
                    time_a = grupo_atual[idx_a]
                    time_b = grupo_atual[idx_b]
                    
                    partida_existente = Match.objects.filter(
                        Q(team_a=time_a, team_b=time_b) | 
                        Q(team_a=time_b, team_b=time_a),
                        tournament=tournament
                    ).exists()
                    
                    if not partida_existente:
                        Match.objects.create(
                            tournament=tournament,
                            category_of_match=category,
                            team_a=time_a,
                            team_b=time_b,
                            location=tournament.local,
                            start_time=datetime.combine(tournament.start_date, datetime.min.time()) + timedelta(hours=9),
                            end_time=datetime.combine(tournament.start_date, datetime.min.time()) + timedelta(hours=10)
                        )

    return redirect('chaves', pk=tournament.pk)

def organizador(request):
    return render(request, 'organizador.html')

def create_tournament_page(request):
    return render(request, 'criar_campeonato.html')

#Organizador 
def criar_torneio(request):
    if request.method != 'POST':
        form = TournamentForm()
    else: 
        form = TournamentForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect('inicio')
    return render(request, 'criar_campeonato.html')