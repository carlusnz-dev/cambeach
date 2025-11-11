from django.shortcuts import render


def inicio(request):
    return render(request, 'cambeach_app/inicio.html')