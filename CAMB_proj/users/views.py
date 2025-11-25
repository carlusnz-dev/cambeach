from django.shortcuts import render, redirect
from .forms import AtletaCreationForm
from django.contrib.auth import login , logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from cambeach_app.models import Team, Match

# cadastro de usuário
def cadastro(request):
    if request.method != 'POST':
        form = AtletaCreationForm()
    else: 
        form = AtletaCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('inicio')

    return render(request=request, template_name='users/cadastro.html', context={'form': form})

# logout de usuário
def logout_view(request):
    logout(request)
    return redirect('inicio')

# perfil do usuário
@login_required
def perfil(request):
    user = request.user
    
    my_teams = Team.objects.filter(players=user).select_related('tournament', 'category')
    all_matches = Match.objects.filter(
        Q(team_a__players=user) | Q(team_b__players=user)
    ).order_by('start_time')
    
    upcoming_matches = all_matches.filter(score_team_a__isnull=True)
    history_matches = all_matches.filter(score_team_a__isnull=False).order_by('-start_time')
    
    total_jogos = history_matches.count()
    total_vitorias = 0
    
    for match in history_matches:
        is_team_a = user in match.team_a.players.all()
        
        if is_team_a and match.score_team_a > match.score_team_b:
            total_vitorias += 1
        elif not is_team_a and match.score_team_b > match.score_team_a:
            total_vitorias += 1

    context = {
        'my_teams': my_teams,
        'upcoming_matches': upcoming_matches,
        'history_matches': history_matches,
        'total_jogos': total_jogos,
        'total_vitorias': total_vitorias
    }
    
    return render(request, 'users/perfil.html', context)