from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.models import Site
from clientes.models import Cliente, DominioCliente
from clientes.forms import ClienteForm

from django.utils.text import slugify
from django.http import HttpResponseRedirect, HttpRequest

from core.views import FormularioGenericoView
from django.conf import settings
from django.urls import reverse

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
    

class CrearClienteView(FormularioGenericoView):
    form_class = ClienteForm
    template_name = 'form_template.html'
    page_title = 'Crear nuevo cliente'
    form_title = 'Registrar cliente nuevo'
    button_text = 'Crear cliente'

    def generar_subdominio_unico(self, nombre):
        base_slug = slugify(nombre)
        slug = base_slug
        num = 1
        while Cliente.objects.filter(dominio__startswith=slug).exists():
            slug = f"{base_slug}-{num}"
            num += 1
        return slug

    def form_valid(self, form):
        nombre_empresa = form.cleaned_data['nombre']
        subdominio = self.generar_subdominio_unico(nombre_empresa)

        environment_mode = os.getenv('ENVIRONMENT', 'development')
        if environment_mode == 'production':
            dominio_completo = f"{subdominio}.balancigastos.com"
            protocolo = "https"
        elif environment_mode == 'staging':
            dominio_completo = f"{subdominio}.staging.balancigastos.com"
            protocolo = "https"
        else:
            dominio_completo = f"{subdominio}.localhost"
            protocolo = "http"

        # Crear el cliente (tenant)
        cliente = form.save(commit=False)
        cliente.schema_name = subdominio
        cliente.dominio = dominio_completo
        cliente.save()

        # Crear dominio del cliente
        DominioCliente.objects.create(
            domain=dominio_completo,
            tenant=cliente,
            is_primary=True
        )

        # Crear objeto Site
        Site.objects.get_or_create(
            domain=dominio_completo,
            defaults={'name': cliente.nombre}
        )

        # Redireccionar al login del subdominio
        login_path = reverse('usuarios:login')
        port = '' if protocolo == 'https' else ':8000'
        redirect_url = f'{protocolo}://{dominio_completo}{port}{login_path}'

        messages.success(self.request, f'Cliente {cliente.nombre} creado exitosamente.')
        return HttpResponseRedirect(redirect_url)