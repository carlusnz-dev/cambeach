from django.db import models

OPCOES_URGENCIA = [
  ('PEQUENA', 'Pequena'),
  ('MEDIA', 'Média'),
  ('GRANDE', 'Grande'),
]

# Create your models here.
class Tarefa(models.Model):
  titulo = models.CharField(max_length=100)
  descricao = models.TextField()
  concluida = models.BooleanField(default=False)
  data_criacao = models.DateTimeField(auto_now_add=True)
  data_vencimento = models.DateTimeField(null=True, blank=True)
  
  urgencia = models.CharField(
    max_length=7,
    choices=OPCOES_URGENCIA,
    default='pequena'
  )
  
  def __str__(self):
    return self.titulo