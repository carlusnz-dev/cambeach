from django.db import models

class Category(models.Model):
  GENDER_CHOISES = [
    (1, 'Masculino'),
    (2, 'Feminino'),
  ]
  
  name = models.CharField(max_length=255, unique=True)
  genre = models.SmallIntegerField(choices=GENDER_CHOISES)
  
  def __str__(self):
    return self.name
  
class Tournament(models.Model):
  name = models.CharField(max_length=255, unique=True)
  local = models.CharField(max_length=255)
  organization = models.CharField(max_length=255)
  enrollment = models.DateField()
  start_date = models.DateField()
  end_date = models.DateField()
  n_players = models.SmallIntegerField()
  categories = models.ManyToManyField(Category)
  
  def __str__(self):
    return self.name
  
class Team(models.Model):
  player_1 = models.ForeignKey("users.User", verbose_name=(""), on_delete=models.CASCADE, related_name="team_of_player_1")
  player_2 = models.ForeignKey("users.User", verbose_name=(""), on_delete=models.CASCADE, related_name="team_of_player_2")
  
  def __str__(self):
    return self.name
  
# class Match: