from django.db import models

# Category
class Gender(models.IntegerChoices):
    MALE = 1, "Masculino"
    FEMALE = 2, "Feminino"
    
class Category(models.Model):
    name = models.CharField(max_length=30, null=False)
    genre = models.SmallIntegerField(choices=Gender)