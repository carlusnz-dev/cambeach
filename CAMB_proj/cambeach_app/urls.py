from django.urls import path 
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    # Torneios
    path('tornament/', views.tornament, name='tornament'),
    path('torneio/<int:tournament_id>/inscrever/', views.inscrever, name='inscrever'),
    path('torneio/<int:pk>/chaves/', views.chaves, name='chaves'),
    path('torneio/<int:pk>/gerar_chaves/', views.gerar_chaves, name='gerar_chaves'),
    path('torneio/create/', views.create_tournament_page, name='create_tournament_page'),
    path('torneio/update/<int:pk>/', views.create_tournament_page, name='create_tournament_page'),
    path('torneio/<int:pk>/gerar_mata_mata/', views.gerar_mata_mata, name='gerar_mata_mata'),
    path('torneio/<int:pk>/gerar_proxima_fase/', views.gerar_proxima_fase, name='gerar_proxima_fase'),

    # Organizador
    path('organizador/', views.organizador, name='organizador'),
    
    # Categoria
    path('category/create/', views.category_form, name='category_create'),
    path('category/update/<int:pk>/', views.category_form, name='category_update'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),
    
    # partida
    path('partida/<int:pk>/placar/', views.atualizar_placar, name='atualizar_placar'),
    path('convite/<int:team_id>/aceitar/', views.aceitar_convite, name='aceitar_convite'),
    path('convite/<int:team_id>/recusar/', views.recusar_convite, name='recusar_convite'),

    # Debug
    path('suporte/', views.suporte, name='suporte'),
    path('torneio/<int:pk>/debug-popular/', views.debug_popular_times, name='debug_popular'),
]