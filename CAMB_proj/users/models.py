from django.db import models
from django.contrib.auth.models import AbstractUser 

class Atleta(AbstractUser):

    username = None 
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 
    
    class genero(models.TextChoices):
        MASCULINO = 'M', 'Masculino'
        FEMININO = 'F', 'Feminino'  
    
    class categoria(models.TextChoices):
        A = 'A', 'A'
        B = 'B', 'B'
        C = 'C', 'C'
        D = 'D', 'D'
        E = 'E', 'E'


    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_de_nascimento = models.DateField(blank=True , null=True)
    
    genero = models.CharField(
        max_length=1,
        choices=genero.choices,
        blank=False , 
        null=False
    )
    
    categoria = models.CharField(
        max_length=1,
        choices=categoria.choices,
        blank=False,
        null =False
    )
        
    def __str__(self):
        return self.email
    

