from django.urls import path 
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    
    # Torneios
    path('torneio/create/', views.tournament_form, name='tournament_create'),
    
    # Categorias
    path('category/create/', views.category_form, name='category_create'),
    path('category/update/<int:pk>/', views.category_form, name='category_update'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),
]
