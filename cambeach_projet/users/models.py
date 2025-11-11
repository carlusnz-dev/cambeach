from django.db import models

class User(models.Model):
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=255)
  name = models.CharField(max_length=255)
  cpf = models.CharField(max_length=14)
  telephone = models.CharField(max_length=14)
  role = models.SmallIntegerField()
  age = models.SmallIntegerField()
  created_at = models.DateTimeField(auto_now_add=True)