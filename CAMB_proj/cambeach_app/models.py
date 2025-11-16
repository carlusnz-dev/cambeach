from django.db import models

# Category
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
    
    # User
    user = models.ForeignKey("users.Atleta", on_delete=models.CASCADE)
    
    # Category
    categories = models.ManyToManyField(Category)