from django.shortcuts import render, redirect
from .forms import DatosPresupuestoForm
from .models import DatosPresupuesto
from django.contrib.auth.decorators import login_required
from django.db.models import F

# Create your views here.

@login_required
def ingresar_datos_generales_presupuesto(request):
    cabecera_presupuesto_form = DatosPresupuestoForm()
    if request.method == "POST":
        cabecera_presupuesto_form = DatosPresupuestoForm(request.POST)
        if cabecera_presupuesto_form.is_valid():
            cabecera_presupuesto_form.save()
            return redirect('presupuestos:presupuestos')
        else:
            cabecera_presupuesto_form = DatosPresupuestoForm()

    return render(request,"presupuestos/datos_cabecera.html",{'cabecera_presupuesto_form':cabecera_presupuesto_form})

@login_required
def lista_presupuestos(request):
    lista_presupuestos = DatosPresupuesto.objects.all()
    return render(request,"presupuestos/lista_presupuestos.html",{'lista_presupuestos':lista_presupuestos})
