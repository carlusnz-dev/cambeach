from django.urls import path 
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    
    # Categorias
    path('create/', views.category_form, name='category_create'),
    path('update/<int:pk>/', views.category_form, name='category_update'),
    path('delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('tornament/', views.tornament, name='tornament'),
]
