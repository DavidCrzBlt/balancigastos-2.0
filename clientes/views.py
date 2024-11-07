from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.models import Site
from clientes.models import Cliente, DominioCliente
from clientes.forms import ClienteForm

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
import os


# Create your views here.

###--------------------------------------------------------------------------------###
###--------------------------------------------------------------------------------###
###--------------------------------------------------------------------------------###

dominio_principal = os.getenv('MAIN_DOMAIN')

def pagina_principal(request):
    # Obtener el dominio actual
    current_site = get_current_site(request)
    print(f'Este es el current site: {current_site}')
    print(f'Este es el dominio principal: {dominio_principal}')

    # Verificar si el dominio es localhost
    if current_site.domain == dominio_principal:
        return redirect('clientes:crear_cliente') 
    else:
        return redirect('usuarios:login')  

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            tenant = form.save(commit=False)
            tenant.schema_name=tenant.nombre
            tenant.save()

            if dominio_principal == 'www.balancigastos.com':
                dominio_principal = 'balancigastos.com'
            # Crear el dominio asociado para el tenant
            dominio_cliente = DominioCliente()
            dominio_cliente.domain = f'{tenant.dominio}.{dominio_principal}'
            dominio_cliente.tenant = tenant
            dominio_cliente.is_primary = True 
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


def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})