from django.db import models
from django.contrib.auth.models import AbstractUser ,Group , Permission

class Atleta(AbstractUser):



    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text=(
            "Os grupos aos quais este atleta pertence. Um atleta terá todas as permissões "
            "concedidas a cada um dos seus grupos."
        ),
        related_name="atleta_groups"  # <--- Este é o novo apelido único
    )

    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        help_text="Permissões específicas para este atleta.",
        related_name="atleta_permissions" # <--- Este é o outro novo apelido
    )
    
    is_arbitro = models.BooleanField(
    default=False 
    )
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    
    CATEGORIA_CHOICES = [
        ('A', 'Categoria A'),
        ('B', 'Categoria B'),
        ('C', 'Categoria C'),
        ('D', 'Categoria D'),
        ('PRO', 'Profissional'),
    ]

    email = models.EmailField(unique=True) 
    nome_completo = models.CharField(max_length=255) 
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, null=True, blank=True)
    categoria = models.CharField(max_length=3, choices=CATEGORIA_CHOICES, null=True, blank=True)
    idade = models.IntegerField(null=True, blank=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    CPF = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username', 'nome_completo'] # Campos pedidos no 'createsuperuser'

    def __str__(self):
        return self.email
    