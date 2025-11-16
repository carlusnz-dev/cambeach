from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Gender
from .forms import CategoryForm

def inicio(request):
    categories = Category.objects.all()
    
    context = {
        'categories': categories
    }
    
    return render(request, 'inicio.html', context)

# Categorias
def category_form(request, pk=None):
    category = None
    
    if pk:
        category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        
        if form.is_valid():
            form.save()
            return redirect('home')
        
    else:
        form = CategoryForm(instance=category)
        
    context = {'form': form, 'category': category}
    return render(request, 'category_form.html', context)

def category_delete(request, pk):
    category = get_object_or_404(Category, pk)
    
    category.delete()
    return redirect('home')