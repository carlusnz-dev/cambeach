from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from .models import Category, Tournament, Team, Match, TournamentDivision, Group
from .forms import CategoryForm, TournamentForm, TeamForm, MatchResultForm
from .utils import calcular_classificacao
import random
import string

def inicio(request):
    tournaments = Tournament.objects.all()
    context = {'tournaments': tournaments}
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
    context = {'tournaments': tournaments}
    return render(request, 'campeonatos.html', context)

@staff_member_required
def gerar_chaves(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    
    data_ingenua = datetime.combine(tournament.start_date, datetime.min.time()) + timedelta(hours=8)
    current_time = timezone.make_aware(data_ingenua)
    
    duracao_jogo = timedelta(minutes=45)
    jogos_simultaneos = 0
    max_quadras = 4 

    divisions = TournamentDivision.objects.filter(tournament=tournament)
    max_teams_per_category = {d.category.id: d.max_teams for d in divisions}
    group_counter = {}

    for category in tournament.categories.all():
        limit = max_teams_per_category.get(category.id, 16)
        teams = list(Team.objects.filter(tournament=tournament, category=category, status=Team.Status.CONFIRMED).order_by('?')[:limit])
        
        group_counter[category.id] = 1 
        
        for i in range(0, len(teams), 4):
            grupo_atual = teams[i : i + 4]
            group_name = f"Grupo {group_counter[category.id]}"
            
            group_obj, _ = Group.objects.get_or_create(
                tournament=tournament,
                category=category,
                name=group_name,
            )
            group_obj.teams.set(grupo_atual)
            group_counter[category.id] += 1

            for idx_a in range(len(grupo_atual)):
                for idx_b in range(idx_a + 1, len(grupo_atual)):
                    if jogos_simultaneos >= max_quadras:
                        current_time += duracao_jogo
                        jogos_simultaneos = 0
                    
                    Match.objects.create(
                        tournament=tournament,
                        category_of_match=category,
                        group=group_obj,
                        team_a=grupo_atual[idx_a],
                        team_b=grupo_atual[idx_b],
                        location=f"{tournament.local} - Quadra {jogos_simultaneos + 1}",
                        start_time=current_time,
                        end_time=current_time + duracao_jogo
                    )
                    jogos_simultaneos += 1
                        
    messages.success(request, "Fase de grupos gerada com sucesso!")
    return redirect('chaves', pk=tournament.pk)

def chaves(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    groups = Group.objects.filter(tournament=tournament).prefetch_related('teams', 'matches_in_group')
    
    groups_data = []
    for group in groups:
        ranking = calcular_classificacao(group)
        groups_data.append({
            'group': group,
            'ranking': ranking
        })

    mata_mata_matches = Match.objects.filter(
        tournament=tournament
    ).exclude(round=Match.Round.GROUP).order_by('start_time', 'id')

    context = {
        'tournament': tournament,
        'groups_data': groups_data,
        'mata_mata_matches': mata_mata_matches
    }
    return render(request, 'chaves.html', context)

def organizador(request):
    return render(request, 'organizador.html')

@login_required
def inscrever(request, tournament_id):
    torneio = get_object_or_404(Tournament, pk=tournament_id)
    
    if request.method == 'POST':
        form = TeamForm(request.POST, tournament=torneio, user=request.user)
        if form.is_valid():
            novo_time = form.save(commit=False)
            novo_time.tournament = torneio
            novo_time.status = Team.Status.PENDING 
            
            parceiro = form.cleaned_data['parceiro_obj']
            novo_time.name = f"{request.user.first_name} & {parceiro.first_name}"
            novo_time.save()
            
            novo_time.players.add(request.user)
            novo_time.players.add(parceiro)
            
            messages.success(request, 'Inscrição realizada! Aguarde seu parceiro aceitar.')
            return redirect('perfil')
    else:
        form = TeamForm(tournament=torneio, user=request.user)
    
    return render(request, 'inscrever.html', {'form': form, 'torneio': torneio})

@login_required
def aceitar_convite(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.user in team.players.all() and team.status == Team.Status.PENDING:
        team.status = Team.Status.CONFIRMED
        team.save()
        messages.success(request, 'Dupla confirmada com sucesso!')
    return redirect('perfil')

@login_required
def recusar_convite(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.user in team.players.all() and team.status == Team.Status.PENDING:
        team.delete()
        messages.info(request, 'Convite recusado.')
    return redirect('perfil')

@staff_member_required
def atualizar_placar(request, pk):
    match = get_object_or_404(Match, pk=pk)
    if request.method == 'POST':
        form = MatchResultForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('chaves', pk=match.tournament.pk)
    else:
        form = MatchResultForm(instance=match)
    return render(request, 'atualizar_placar.html', {'form': form, 'match': match})

@staff_member_required
def gerar_mata_mata(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    data_base = datetime.combine(tournament.end_date, datetime.min.time()) + timedelta(hours=14)
    start_time = timezone.make_aware(data_base)
    
    for category in tournament.categories.all():
        if Match.objects.filter(tournament=tournament, category_of_match=category).exclude(round=Match.Round.GROUP).exists():
            continue

        groups = Group.objects.filter(tournament=tournament, category=category)
        classificados = []
        for group in groups:
            ranking = calcular_classificacao(group)
            if len(ranking) >= 2:
                classificados.append(ranking[0]['team']) 
                classificados.append(ranking[1]['team']) 
        
        qtd_classificados = len(classificados)
        
        if qtd_classificados == 0:
            continue

        fase = Match.Round.QUARTAS
        if qtd_classificados > 8:
            fase = Match.Round.OITAVAS
        elif qtd_classificados <= 4 and qtd_classificados > 2:
            fase = Match.Round.SEMI
        elif qtd_classificados == 2:
            fase = Match.Round.FINAL

        for i in range(0, qtd_classificados, 2):
            if i + 1 < qtd_classificados:
                Match.objects.create(
                    tournament=tournament,
                    category_of_match=category,
                    team_a=classificados[i],
                    team_b=classificados[i+1],
                    round=fase,
                    start_time=start_time,
                    end_time=start_time + timedelta(minutes=60),
                    location=f"{tournament.local} - Quadra Principal"
                )
    
    messages.success(request, "Fase eliminatória gerada com sucesso!")
    return redirect('chaves', pk=tournament.pk)

@staff_member_required
def gerar_proxima_fase(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    
    fluxo_fases = {
        Match.Round.OITAVAS: Match.Round.QUARTAS,
        Match.Round.QUARTAS: Match.Round.SEMI,
        Match.Round.SEMI: Match.Round.FINAL
    }

    for category in tournament.categories.all():
        ultima_rodada = Match.objects.filter(
            tournament=tournament, 
            category_of_match=category
        ).exclude(round=Match.Round.GROUP).order_by('-id').first()

        if not ultima_rodada:
            continue
            
        fase_atual = ultima_rodada.round
        if fase_atual not in fluxo_fases:
            continue

        proxima_fase = fluxo_fases[fase_atual]
        
        if Match.objects.filter(tournament=tournament, category_of_match=category, round=proxima_fase).exists():
            continue

        jogos_fase_atual = Match.objects.filter(
            tournament=tournament, 
            category_of_match=category, 
            round=fase_atual
        ).order_by('id')
        
        vencedores = []
        todas_finalizadas = True
        
        for match in jogos_fase_atual:
            if match.score_team_a is None or match.score_team_b is None:
                todas_finalizadas = False
                break
            
            if match.score_team_a > match.score_team_b:
                vencedores.append(match.team_a)
            else:
                vencedores.append(match.team_b)
        
        if todas_finalizadas and len(vencedores) >= 2:
            start_time = timezone.now() + timedelta(hours=1)
            for i in range(0, len(vencedores), 2):
                if i+1 < len(vencedores):
                    Match.objects.create(
                        tournament=tournament,
                        category_of_match=category,
                        team_a=vencedores[i],
                        team_b=vencedores[i+1],
                        round=proxima_fase,
                        start_time=start_time,
                        end_time=start_time + timedelta(minutes=60),
                        location=tournament.local
                    )

    messages.success(request, "Próxima fase gerada!")
    return redirect('chaves', pk=pk)

def suporte(request):
    return render(request, 'suporte.html')

def random_string(length=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def random_cpf():
    return f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"

@staff_member_required
def debug_popular_times(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    Atleta = get_user_model() 
    
    limite_global = tournament.n_players 

    for category in tournament.categories.all():
        total_inscritos_torneio = Team.objects.filter(tournament=tournament).count()
        
        if total_inscritos_torneio >= limite_global:
            break 

        divisao = tournament.divisions.filter(category=category).first()
        limite_categoria = divisao.max_teams if divisao else 16
        
        inscritos_categoria = Team.objects.filter(
            tournament=tournament, 
            category=category
        ).count()
        
        vagas_na_categoria = limite_categoria - inscritos_categoria
        vagas_no_torneio = limite_global - total_inscritos_torneio
        
        quantidade_times_para_criar = min(vagas_na_categoria, vagas_no_torneio)
        
        if quantidade_times_para_criar <= 0:
            continue

        for i in range(quantidade_times_para_criar):
            nome_1 = f"Bot_{random_string()}"
            email_1 = f"{nome_1}@debug.com"
            atleta1, created1 = Atleta.objects.get_or_create(
                email=email_1,
                defaults={'first_name': nome_1, 'last_name': 'Debug', 'cpf': random_cpf()}
            )
            if created1:
                atleta1.set_password('123')
                atleta1.save()

            nome_2 = f"Bot_{random_string()}"
            email_2 = f"{nome_2}@debug.com"
            atleta2, created2 = Atleta.objects.get_or_create(
                email=email_2,
                defaults={'first_name': nome_2, 'last_name': 'Debug', 'cpf': random_cpf()}
            )
            if created2:
                atleta2.set_password('123')
                atleta2.save()

            nome_time = f"Dupla Debug {random_string(3).upper()}"
            team = Team.objects.create(
                name=nome_time,
                tournament=tournament,
                category=category,
                status=Team.Status.CONFIRMED
            )
            team.players.add(atleta1, atleta2)

    messages.success(request, f"Torneio preenchido respeitando o limite global de {limite_global} duplas!")
    return redirect('chaves', pk=tournament.pk)