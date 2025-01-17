from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse

from .forms import DatosPresupuestoForm, PreciosUnitariosForm
from .models import DatosPresupuesto,PrecioUnitarioPresupuesto, HistorialPresupuesto
from usuarios.models import Profile
from .utils import generar_pdf

import json
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
    presupuesto_object = get_object_or_404(DatosPresupuesto,slug=slug)
    if request.method == "POST":
        precios_unitarios_form = PreciosUnitariosForm(request.POST)
        print(request.POST)
        if precios_unitarios_form.is_valid():
            pu = precios_unitarios_form.save(commit=False)
            pu.presupuesto = presupuesto_object
            pu.save()
            messages.success(request,f'Se agrego exitosamente el concepto')
            return redirect('presupuestos:ingresar_precios_unitarios',slug=slug)
        else:
            messages.error(request,f'Hay un error con el formulario')
            return render(request, "presupuestos/precios_unitarios.html", {
        'precios_unitarios_form': precios_unitarios_form,
        'presupuesto': presupuesto_object
    })

    return render(request,"presupuestos/precios_unitarios.html",{'precios_unitarios_form':precios_unitarios_form,'presupuesto':presupuesto_object})

@login_required
def ajuste_presupuesto(request,slug):

    presupuesto = DatosPresupuesto.objects.get(slug=slug)
    historial_reciente = HistorialPresupuesto.objects.filter(presupuesto=presupuesto).order_by('-version').first()

    if historial_reciente:
        return redirect('presupuestos:presupuesto',slug=slug,version=historial_reciente.version)
    else:
        conceptos = PrecioUnitarioPresupuesto.objects.filter(presupuesto=presupuesto)

        # Generar la URL para confirmar presupuesto y pasarlo al contexto
        confirmar_presupuesto_url = reverse('presupuestos:confirmar_presupuesto', kwargs={'slug': 'slug_placeholder'})
        return render(request,"presupuestos/ajuste_presupuesto.html",{'conceptos':conceptos,'presupuesto':presupuesto,'confirmar_presupuesto_url':confirmar_presupuesto_url})

@login_required
def confirmar_presupuesto(request,slug):
    presupuesto = get_object_or_404(DatosPresupuesto,slug=slug)

    if request.method == 'POST':
        
        data = json.loads(request.body)
        precios_unitarios_ids = data.get('precios_unitarios_ids', [])
        precios_unitarios_ids = [int(id) for id in precios_unitarios_ids]


        # Lógica para calcular la versión
        ultima_version = HistorialPresupuesto.objects.filter(presupuesto=presupuesto).order_by('-version').first()
        nueva_version = (ultima_version.version + 1) if ultima_version else 1

        # Datos cabecera del presupuesto
        datos_cabecera = {
            "num_presupuesto":presupuesto.num_presupuesto,
            "nombre_proyecto":presupuesto.nombre_proyecto,
            "cliente":presupuesto.cliente,
            "responsable":presupuesto.responsable,
            "contacto":presupuesto.contacto,
            "fecha":str(presupuesto.fecha),
            "version":nueva_version
        }

        # Todas las partidas del presupuesto con subtotales
        partidas_presupuesto = []

        ##Precios unitarios ids debe ser lo que va a recuperar de js

        for partida in presupuesto.precio_unitario.filter(id__in=precios_unitarios_ids):
            partidas_presupuesto.append({
                "concepto": partida.concepto,
                "unidad": partida.unidad,
                "materiales": float(partida.materiales),
                "mano_obra": float(partida.mano_obra),
                "examenes_med_dc3": float(partida.examenes_med_dc3),
                "equipos": float(partida.equipos),
                "epp": float(partida.epp),
                "costo_directo": float(partida.costo_directo),
                "costo_indirecto": float(partida.costo_indirecto),
                "costo_financiamiento": float(partida.costo_financiamiento),
                "meses_financiamiento": float(partida.meses_financiamiento),
                "utilidad": float(partida.utilidad),
                "precio_unitario": float(partida.precio_unitario),
                "cantidad":float(partida.cantidad),
                "subtotal":float(partida.subtotal),
            })

        # Calcular subtotal, IVA 16% y total general
        subtotal = sum(item["subtotal"] for item in partidas_presupuesto)
        iva = subtotal * 0.16
        total_general = subtotal + iva

        totales = {
            "subtotal":round(subtotal,2),
            "iva":round(iva,2),
            "total_general":round(total_general,2)
        }

        json_completo = {
            "datos_cabecera":datos_cabecera,
            "partidas_presupuesto":partidas_presupuesto,
            "totales":totales
        }


        historial = HistorialPresupuesto.objects.create(
            presupuesto = presupuesto,
            version = nueva_version,
            presupuesto_json = json_completo,
        )

        historial.save()

        return JsonResponse({'success': True, 'redirect_url': reverse('presupuestos:presupuesto', kwargs={'slug': slug, 'version': nueva_version})})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def presupuesto(request,slug,version):

    presupuesto = get_object_or_404(DatosPresupuesto,slug=slug)
    version_presupuesto = get_object_or_404(HistorialPresupuesto,presupuesto=presupuesto,version=version)

    json_presupuesto = version_presupuesto.presupuesto_json

    return render(request,"presupuestos/presupuesto.html",{"json_presupuesto":json_presupuesto,"slug":slug,"version":version})

@login_required
def lista_presupuestos(request):
    lista_presupuestos = DatosPresupuesto.objects.all()
    return render(request,"presupuestos/lista_presupuestos.html",{'lista_presupuestos':lista_presupuestos})

@login_required
def generar_pdf_vista(request, slug, version):

    presupuesto = DatosPresupuesto.objects.get(slug=slug)
    print_version = HistorialPresupuesto.objects.get(presupuesto=presupuesto,version=version)
    profile = Profile.objects.get(user=request.user)

    imagen_url = profile.profile_picture.url  # Esto te da la URL relativa

    absolute_imagen_url = request.build_absolute_uri(imagen_url)
    
    # Datos para el contexto
    context = print_version.presupuesto_json

    datos_cabecera = context["datos_cabecera"]
    datos_pu = context["partidas_presupuesto"]
    totales = context["totales"]
    datos_cotizacion = {
        "num_presupuesto":datos_cabecera["num_presupuesto"],
        "cliente":datos_cabecera["cliente"],
        "responsable":datos_cabecera["responsable"],
        "fecha":datos_cabecera["fecha"],
        "datos_pu":datos_pu,
        "subtotal":totales["subtotal"],
        "iva":totales["iva"],
        "total":totales["total_general"],
        'absolute_imagen_url': absolute_imagen_url
    }

    filename = f'{presupuesto.num_presupuesto}.pdf'
    # Generar el PDF
    pdf_path = generar_pdf("presupuestos/presupuesto_sample.html", datos_cotizacion, filename,request,profile)
    
    # Devolver el archivo PDF como respuesta
    with open(pdf_path, "rb") as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type="application/pdf")
        response['Content-Disposition'] = f'inline; filename={filename}'
        return response
