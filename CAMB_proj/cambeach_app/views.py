from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Category, Tournament, Team, Match, TournamentDivision
from .forms import CategoryForm, TournamentForm, TeamForm
import random
import string

# pagina inicial 

def inicio(request):
    tournaments = Tournament.objects.all()
    context = {
        'tournaments': tournaments
    }
    return render(request, 'inicio.html', context)

# categoria

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


# torneio
@login_required
def create_tournament_page(request, pk=None):
    tournament = None
    if pk:
        tournament = get_object_or_404(Tournament, pk=pk)
    
    if request.method == 'POST':
        form = TournamentForm(request.POST, instance=tournament)
        
        if form.is_valid():
            tournament = form.save(commit=False)
            data = form.cleaned_data['categories']
            form.save()
            
            for i in data:
                tournament_division = tournament.divisions.filter(category=i).first()
                if not tournament_division:
                    tournament.divisions.create(category=i, max_teams=16)
            
            return redirect('create_tournament_page')
    else:
        form = TournamentForm(instance=tournament)
        
    context = {'form': form, 'tournament': tournament}
    return render(request, 'criar_campeonato.html', context)

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

@login_required
def gerar_chaves(request, pk):
    from datetime import datetime, timedelta
    import random
    from django.shortcuts import get_object_or_404, redirect
    from .models import Tournament, Team, Match, TournamentDivision, Category, Group, Q # Q deve ser importado
    from django.db.models import Q

    tournament = get_object_or_404(Tournament, pk=pk)
    
    max_teams_per_category = {}
    divisions = TournamentDivision.objects.filter(tournament=tournament)
    for division in divisions:
        max_teams_per_category[division.category.id] = division.max_teams
    
    group_counter = {}

    for category in tournament.categories.all():
        limit = max_teams_per_category.get(category.id, 16)
        teams_all = list(Team.objects.filter(tournament=tournament, category=category))
        
        for t in teams_all:
            t.sort_key = random.random()
        teams_all.sort(key=lambda x: x.sort_key)
        
        teams = teams_all[:limit]
        
        group_counter[category.id] = 1 
        
        for i in range(0, len(teams), 5):
            grupo_atual = teams[i : i + 5]
            
            group_name = f"Grupo {group_counter[category.id]}"
            
            group_obj, created = Group.objects.get_or_create(
                tournament=tournament,
                category=category,
                name=group_name,
            )
            
            group_obj.teams.set(grupo_atual)
            
            group_counter[category.id] += 1

            for idx_a in range(len(grupo_atual)):
                for idx_b in range(idx_a + 1, len(grupo_atual)):
                    time_a = grupo_atual[idx_a]
                    time_b = grupo_atual[idx_b]
                    
                    partida_existente = Match.objects.filter(
                        Q(team_a=time_a, team_b=time_b) | 
                        Q(team_a=time_b, team_b=time_a),
                        tournament=tournament,
                        category_of_match=category
                    ).exists()
                    
                    if not partida_existente:
                        Match.objects.create(
                            tournament=tournament,
                            category_of_match=category,
                            group=group_obj, 
                            team_a=time_a,
                            team_b=time_b,
                            location=tournament.local,
                            start_time=datetime.combine(tournament.start_date, datetime.min.time()) + timedelta(hours=9),
                            end_time=datetime.combine(tournament.start_date, datetime.min.time()) + timedelta(hours=10)
                        )
                        
    return redirect('chaves', pk=tournament.pk)

def chaves(request, pk):
    from django.shortcuts import get_object_or_404, render
    from .models import Tournament, Match, Group # Importe Group

    tournament = get_object_or_404(Tournament, pk=pk)
    
    groups = Group.objects.filter(tournament=tournament).order_by('category', 'id')
    
    matches = Match.objects.filter(tournament=tournament).order_by('category_of_match', 'group', 'id')

    context = {
        'tournament': tournament,
        'matches': matches,
        'groups': groups 
    }
    return render(request, 'chaves.html', context)

def organizador(request):
    return render(request, 'organizador.html')

# @login_required
# def create_tournament_page(request):
#     if request.method != 'POST':
#         form = TournamentForm()
#     else: 
#         form = TournamentForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('inicio')
#     context = {'form': form}
#     return render(request, 'criar_campeonato.html', context)

# inscrição no torneio
@login_required
def inscrever(request, tournament_id):
    torneio = get_object_or_404(Tournament, pk=tournament_id)
    
    if request.method == 'POST':
        form = TeamForm(request.POST, tournament=torneio, user=request.user)
        if form.is_valid():
            novo_time = form.save(commit=False)
            novo_time.tournament = torneio
            parceiro = form.cleaned_data['parceiro_obj']
            novo_time.name = f"Dupla {request.user.first_name} & {parceiro.first_name}"
            novo_time.save()
            novo_time.players.add(request.user)
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

def suporte(request):
    return render('suporte', 'suporte.html')