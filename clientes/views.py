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

def get_subdomain(request: HttpRequest):
    # Obtener el hostname completo (subdominio.dominio.com)
    host = request.get_host()
    
    # Dividir el hostname por puntos
    parts = host.split('.')
    
    # Asegurarse de que tiene el formato correcto (subdominio.dominio.tld)
    if len(parts) >= 3:
        # El subdominio será la primera parte
        subdomain = parts[0]
    else:
        # Si no hay subdominio, devolver None o algún valor predeterminado
        subdomain = None

    return subdomain

def pagina_principal(request):
    # Obtener el dominio actual
    current_site = get_current_site(request)
    subdomain = get_subdomain(request)
    print(f'Este es el current site: {current_site}')
    print(f'Este es el dominio principal: {dominio_principal}')
    print(f'Función de subdomain: {subdomain} ')
    # Verificar si el dominio es localhost
    if current_site.domain == dominio_principal:
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

    return render(request, 'clientes/crear_cliente.html', {'form': form,'current_site':get_current_site(request),'dominio_principal':dominio_principal,'subdomain':get_subdomain(request)})

#
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})