from django.shortcuts import render

def home(request):
  return render(request, 'cambeach_app/inicio.html')