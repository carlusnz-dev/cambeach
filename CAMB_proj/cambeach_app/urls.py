from django.urls import path 
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    # Torneio
    path('tornament/', views.tornament, name='tornament'),
    path('torneio/<int:tournament_id>/inscrever/', views.inscrever, name='inscrever'),
    path('torneio/<int:pk>/chaves/', views.chaves, name='chaves'),
    path('torneio/<int:pk>/gerar_chaves/', views.gerar_chaves, name='gerar_chaves'),
    path('torneio/create/', views.tournament_form, name='tournament_create'),
    path('torneio/update/<int:pk>/', views.tournament_form, name='tournament_edit'),

    # Organizador
    path('organizador/', views.organizador, name='organizador'),
    path('create_tournament_page/', views.create_tournament_page, name='create_tournament_page'),
    
    # Categoria
    path('category/create/', views.category_form, name='category_create'),
    path('category/update/<int:pk>/', views.category_form, name='category_update'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),
    
    # Debug
    path('torneio/<int:pk>/debug-popular/', views.debug_popular_times, name='debug_popular'),
]