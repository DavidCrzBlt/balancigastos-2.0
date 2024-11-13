from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.models import Site
from clientes.models import Cliente, DominioCliente
from clientes.forms import ClienteForm

from django.http import HttpResponseRedirect, HttpRequest

import os


# Create your views here.

###--------------------------------------------------------------------------------###
###--------------------------------------------------------------------------------###
###--------------------------------------------------------------------------------###

dominio_principal = os.getenv('MAIN_DOMAIN')
environment_mode = os.getenv('ENVIRONMENT')

def get_subdomain(request: HttpRequest):
    # Obtener el hostname completo (subdominio.dominio.com)
    subdomain = request.get_host()
    return subdomain

def pagina_principal(request):
    # Dependiendo del dominio va a redireccionar a la página de usuarios o de clientes
    print(f'Dominio principal: {dominio_principal}')
    print(f'Subdomain request: {get_subdomain(request)}')

    if dominio_principal == get_subdomain(request):
        return redirect('clientes:crear_cliente')
    else:
        return redirect('usuarios:login')

def crear_cliente(request):

    pagina_principal(request)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            if environment_mode == 'production':
                dominio_completo = '.balancigastos.com'
            elif environment_mode == 'staging':
                dominio_completo = '.staging.balancigastos.com'
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
            if environment_mode in ('production','staging'):
                liga_redirect = f'https://{dominio_cliente.domain}/usuarios'
            else:
                liga_redirect = f'http://{dominio_cliente.domain}:8000/usuarios'
            
            return HttpResponseRedirect(liga_redirect)
    else:
        form = ClienteForm()

    return render(request, 'clientes/crear_cliente.html', {'form': form})
