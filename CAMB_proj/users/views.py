from django.shortcuts import render, redirect
from .forms import AtletaCreationForm # Importe o formulário que criamos


def login(request):
    return render(request, 'users/login.html')

def cadastro(request):
    from django.shortcuts import render, redirect
from .forms import AtletaCreationForm # Importe o formulário que criamos

def cadastro(request):
    if request.method == 'POST':
        form = AtletaCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = AtletaCreationForm()
    
    return render(request, 'users/cadastro.html', {'form': form})