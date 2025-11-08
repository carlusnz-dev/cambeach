from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Tarefa
from .forms import FormTarefa

# Create your views here.
def lista_tarefas(req):
  tarefas = Tarefa.objects.all()
  
  context = {
    'tarefas': tarefas
  }
  
  return render(req, 'core/lista_tarefas.html', context)

def adicionar_tarefa(req):
  
  if req.method == 'POST':
    form = FormTarefa(req.POST)
    
    if form.is_valid():
      form.save()
      return redirect('lista_tarefas')
  else:
    form = FormTarefa()
  
  context = {
    'form': form
  }
  
  return render(req, 'core/adicionar_tarefa.html', context)