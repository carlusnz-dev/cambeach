from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
]
