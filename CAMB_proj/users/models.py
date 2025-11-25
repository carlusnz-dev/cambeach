from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# atleta manager
class AtletaManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# atleta model
class Atleta(AbstractUser):

    username = None 
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 
    
    # class Genero(models.TextChoices): # Use um nome único para a classe
    #     MASCULINO = 'M', 'Masculino'
    #     FEMININO = 'F', 'Feminino'  
        
    # genero = models.CharField(
    #     max_length=1,
    #     choices=Genero.choices,
    #     blank=False,
    # )
        
    categoria_de_jogo = models.ForeignKey('cambeach_app.Category', on_delete=models.SET_NULL, null=True) 

    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_de_nascimento = models.DateField(blank=True , null=True)
    
    def __str__(self):
        return self.email
    
    objects = AtletaManager()
    
