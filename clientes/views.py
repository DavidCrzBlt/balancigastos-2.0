from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.models import Site
from clientes.models import Cliente, DominioCliente
from clientes.forms import ClienteForm

from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
import os


# Create your views here.

###--------------------------------------------------------------------------------###
###--------------------------------------------------------------------------------###
###--------------------------------------------------------------------------------###

dominio_principal = os.getenv('MAIN_DOMAIN')
environment_mode = os.getenv('ENVIRONMENT')

def pagina_principal(request):
    # Obtener el dominio actual
    current_site = get_current_site(request)
    
    # Verificar si el dominio es localhost o el dominio principal sin subdominios adicionales
    if dominio_principal in current_site.domain or 'localhost' in current_site.domain:
        return redirect('clientes:crear_cliente')
    else:
        return redirect('usuarios:login')

def crear_cliente(request):

    # Schema names and domain names have different validation rules. Underscores (_) and capital letters are permitted in schema names but they are illegal for domain names! On the other hand domain names may contain a dash (-) which is illegal for schema names!

    # You must be careful if using schema names and domain names interchangeably in your multi-tenant applications! The tenant and domain model classes, creation and validation of input data are something that you need to handle yourself, possibly imposing additional constraints to the acceptable values!
    pagina_principal(request)
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            if environment_mode == 'production':
                dominio_completo = '.balancigastos.com'
            else:
                dominio_completo = '.localhost'

            tenant = form.save(commit=False)
            tenant.schema_name=tenant.nombre
            tenant.dominio = tenant.dominio + dominio_completo
            tenant.save()
            print(f'Dominio de tenant completo: {tenant.dominio}')
            
            # Crear el dominio asociado para el tenant
            dominio_cliente = DominioCliente(
            domain = tenant.dominio,
            tenant = tenant,
            is_primary = True
            )
            dominio_cliente.save()
            # Crear el objeto Site para el tenant
            Site.objects.get_or_create(domain=dominio_cliente.domain, defaults={'name': tenant.nombre})

            messages.success(request, f'Cliente {tenant.nombre} creado exitosamente.')
            return HttpResponseRedirect(f'https://{dominio_cliente.domain}/usuarios')
            # En pruebas locales comentar arriba y descomentar abajo
            # return HttpResponseRedirect(f'http://{dominio_cliente.domain}:8000/usuarios')
    else:
        form = ClienteForm()

    return render(request, 'clientes/crear_cliente.html', {'form': form})

#
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})