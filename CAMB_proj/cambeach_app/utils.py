def calcular_classificacao(group):
    stats = {}
    for team in group.teams.all():
        stats[team.id] = {
            'team': team,
            'points': 0,
            'wins': 0,
            'games_balance': 0
        }
    
    matches = group.matches_in_group.all()
    
    for match in matches:
        if match.score_team_a is None or match.score_team_b is None:
            continue
            
        id_a = match.team_a.id
        id_b = match.team_b.id
        
        if id_a not in stats:
            stats[id_a] = {
                'team': match.team_a, 'points': 0, 'wins': 0, 'games_balance': 0
            }
        
        if id_b not in stats:
            stats[id_b] = {
                'team': match.team_b, 'points': 0, 'wins': 0, 'games_balance': 0
            }
        
        diff = match.score_team_a - match.score_team_b
        stats[id_a]['games_balance'] += diff
        stats[id_b]['games_balance'] -= diff
        
        if match.score_team_a > match.score_team_b:
            stats[id_a]['wins'] += 1
            stats[id_a]['points'] += 3
        elif match.score_team_b > match.score_team_a:
            stats[id_b]['wins'] += 1
            stats[id_b]['points'] += 3

    ranking = sorted(
        stats.values(), 
        key=lambda x: (x['points'], x['wins'], x['games_balance']), 
        reverse=True
    )
    
    return ranking