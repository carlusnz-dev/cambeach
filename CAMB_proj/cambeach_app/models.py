from django.db import models

class Gender(models.IntegerChoices):
    MALE = 1, "Masculino"
    FEMALE = 2, "Feminino"
    
class Category(models.Model):
    name = models.CharField(max_length=30, null=False)
    genre = models.SmallIntegerField(choices=Gender)
    
    def __str__(self):
        return self.name

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    local = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    n_players = models.SmallIntegerField()
    categories = models.ManyToManyField(Category, related_name="tournaments")

    def __str__(self):
        return self.name

class TournamentDivision(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="divisions")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="divisions")
    max_teams = models.SmallIntegerField(default=16, verbose_name="Maximo de duplas")

class Team(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nome da Dupla", null=True, blank=True)    
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="teams")
    players = models.ManyToManyField("users.Atleta", related_name="teams")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="teams")

    def __str__(self):
        if self.pk:
            try:
                nomes = list(self.players.values_list('first_name', flat=True))
                if nomes:
                    return " / ".join(nomes)
            except Exception:
                pass
        
        return f"Time {self.pk} (Em formação)"
class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="matches")
    category_of_match = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="matches")
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_a_matches")
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_b_matches")
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    location = models.CharField(max_length=255)
    score_team_a = models.SmallIntegerField(null=True, blank=True)
    score_team_b = models.SmallIntegerField(null=True, blank=True)