from django.shortcuts import render
from datetime import datetime

def landing_view(request):
    return render(request, 'webpublica/landing.html', {'year': datetime.now().year})

def inicio_view(request):
    return render(request, 'webpublica/inicio.html', {'year': datetime.now().year})