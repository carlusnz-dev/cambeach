from datetime import datetime, timedelta
from random import shuffle
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Category, Tournament, Team, Match
from .forms import CategoryForm, TournamentForm, TeamForm
import random
import string

def inicio(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'inicio.html', context)

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

@login_required
def tournament_form(request, pk=None):
    tournament = None
    if pk:
        tournament = get_object_or_404(Tournament, pk=pk)
    
    if request.method == 'POST':
        form = TournamentForm(request.POST, instance=tournament)
        if form.is_valid():
            tournament = form.save(commit=False)
            form.save()
            form.save_m2m()
            return redirect('tournament_create')
    else:
        form = TournamentForm(instance=tournament)
        
    context = {'form': form, 'tournament': tournament}
    return render(request, 'tournament_form.html', context)

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
    teams = Team.objects.filter(tournament=tournament).order_by('category', 'id').prefetch_related('players')
    matches = Match.objects.filter(tournament=tournament).order_by('category_of_match', 'id')

    context = {
        'tournament': tournament,
        'teams': teams,
        'matches': matches
    }
    return render(request, 'chaves.html', context)

@login_required
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
    if request.method != 'POST':
        form = TournamentForm()
    else: 
        form = TournamentForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    context = {'form': form}
    return render(request, 'criar_campeonato.html', context)

@login_required
def inscrever(request, tournament_id):
    torneio = get_object_or_404(Tournament, pk=tournament_id)
    
    if request.method == 'POST':
        form = TeamForm(request.POST, tournament=torneio, user=request.user)
        if form.is_valid():
            novo_time = form.save(commit=False)
            novo_time.tournament = torneio
            novo_time.save() 
            novo_time.players.add(request.user)
            parceiro = form.cleaned_data['parceiro_obj']
            novo_time.players.add(parceiro)
            return redirect('chaves', pk=torneio.pk)
    else:
        form = TeamForm(tournament=torneio, user=request.user)
    
    return render(request, 'inscrever.html', {'form': form, 'torneio': torneio})


# Debug
def random_string(length=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def random_cpf():
    return f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"

def debug_popular_times(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    Atleta = get_user_model() 

    for category in tournament.categories.all():
        
        quantidade_times_para_criar = 16
        
        for i in range(quantidade_times_para_criar):
            nome_1 = f"Bot_{random_string()}"
            email_1 = f"{nome_1}@debug.com"
            
            atleta1, created1 = Atleta.objects.get_or_create(
                email=email_1,
                defaults={
                    'first_name': nome_1, 
                    'last_name': 'Debug',
                    'genero': 'M',
                    'cpf': random_cpf() 
                }
            )
            if created1:
                atleta1.set_password('123')
                atleta1.save()

            nome_2 = f"Bot_{random_string()}"
            email_2 = f"{nome_2}@debug.com"
            
            atleta2, created2 = Atleta.objects.get_or_create(
                email=email_2,
                defaults={
                    'first_name': nome_2,
                    'last_name': 'Debug',
                    'genero': 'M',
                    'cpf': random_cpf()
                }
            )
            if created2:
                atleta2.set_password('123')
                atleta2.save()

            nome_time = f"Dupla Debug {random_string(3).upper()}"
            
            team = Team.objects.create(
                name=nome_time,
                tournament=tournament,
                category=category
            )
            
            team.players.add(atleta1, atleta2)

    return redirect('chaves', pk=tournament.pk)