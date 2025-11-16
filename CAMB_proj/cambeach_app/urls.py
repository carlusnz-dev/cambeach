from django.urls import path 
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    
    # Torneios
    path('tornament', views.tournament, name='tornament'),
    path('torneio/create/', views.tournament_form, name='tournament_create'),
    path('torneio/update/<int:pk>/', views.tournament_form, name='tournament_edit'),
    
    # Categorias
    path('category/create/', views.category_form, name='category_create'),
    path('category/update/<int:pk>/', views.category_form, name='category_update'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('tornament/' ,  views.tornament, name='tornament'),
    path('organizador/', views.organizador, name='organizador'),
    path('create_tournament_page/', views.create_tournament_page, name='create_tournament_page'),
    path('chaves/', views.chaves, name='chaves'),
]
