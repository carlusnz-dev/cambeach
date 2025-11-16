from django.shortcuts import render, redirect
from .forms import AtletaCreationForm
from django.contrib.auth import login , logout


def cadastro(request):
    if request.method != 'POST':
        form = AtletaCreationForm()
    else: 
        form = AtletaCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('inicio')
        
    
    
    return render(request=request, template_name='users/cadastro.html', context={'form': form})

def logout_view(request):
    logout(request)
    return redirect('inicio')