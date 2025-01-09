from django.shortcuts import render, redirect
from .forms import DatosPresupuestoForm, PreciosUnitariosForm
from .models import DatosPresupuesto,PrecioUnitarioPresupuesto, HistorialPresupuesto
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def ingresar_datos_generales_presupuesto(request):
    cabecera_presupuesto_form = DatosPresupuestoForm()
    if request.method == "POST":
        cabecera_presupuesto_form = DatosPresupuestoForm(request.POST)
        if cabecera_presupuesto_form.is_valid():
            datos_presupuesto = cabecera_presupuesto_form.save()
            slug = datos_presupuesto.slug
            return redirect('presupuestos:ingresar_precios_unitarios',slug=slug)
        else:
            cabecera_presupuesto_form = DatosPresupuestoForm()

    return render(request,"presupuestos/datos_cabecera.html",{'cabecera_presupuesto_form':cabecera_presupuesto_form})

@login_required
def ingresar_precios_unitarios(request,slug):
    precios_unitarios_form = PreciosUnitariosForm()
    presupuesto = DatosPresupuesto.objects.get(slug=slug)
    if request.method == "POST":
        precios_unitarios_form = PreciosUnitariosForm(request.POST)
        if precios_unitarios_form.is_valid():
            pu = precios_unitarios_form.save(commit=False)
            pu.presupuesto = presupuesto
            pu.save()
            return redirect('presupuestos:ingresar_precios_unitarios',slug=slug)
        else:
            precios_unitarios_form = PreciosUnitariosForm()

    return render(request,"presupuestos/precios_unitarios.html",{'precios_unitarios_form':precios_unitarios_form,'presupuesto':presupuesto})

@login_required
def ajuste_presupuesto(request,slug):
    presupuesto = DatosPresupuesto.objects.get(slug=slug)
    conceptos = PrecioUnitarioPresupuesto.objects.filter(presupuesto=presupuesto)
    return render(request,"presupuestos/ajuste_presupuesto.html",{'conceptos':conceptos,'presupuesto':presupuesto})

@login_required
def lista_presupuestos(request):
    lista_presupuestos = DatosPresupuesto.objects.all()
    return render(request,"presupuestos/lista_presupuestos.html",{'lista_presupuestos':lista_presupuestos})