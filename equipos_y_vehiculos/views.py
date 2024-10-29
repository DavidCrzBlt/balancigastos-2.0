from django.shortcuts import render, redirect
from .forms import VehiculosForm
from .models import Vehiculos
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,"equipos_y_vehiculos/index.html")

@login_required
def registro_vehiculos(request):

    vehiculos = Vehiculos.objects.all()

    if request.method == "POST":
        vehiculos_form = VehiculosForm(request.POST)

        if vehiculos_form.is_valid():
            vehiculos_form.save()
            return redirect('equipos_y_vehiculos:registro_vehiculos')
    else:
        vehiculos_form = VehiculosForm()

    return render(request,'equipos_y_vehiculos/registrar_vehiculo.html',{'vehiculos_form':vehiculos_form,'vehiculos':vehiculos})