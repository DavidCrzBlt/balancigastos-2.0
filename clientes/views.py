from django.contrib import messages
from django.contrib.sites.models import Site
from django.utils.text import slugify
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView

from core.views import FormularioGenericoView

from clientes.models import Cliente, DominioCliente
from clientes.forms import ClienteForm
from clientes. utils import get_subdomain

import os


# Create your views here.
###--------------------------------------------------------------------------------###

dominio_principal = os.getenv('MAIN_DOMAIN')
environment_mode = os.getenv('ENVIRONMENT')  

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
    
##---------------------- Las siguientes clases aún no están operativas------------##

class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/lista_clientes.html'  # Esta plantilla aún no existe
    context_object_name = 'clientes'

class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'form_template.html'
    success_url = reverse_lazy('clientes:lista_clientes')  #Esta ruta aún no existe

    page_title = 'Editar cliente'
    form_title = 'Editar información del cliente'
    button_text = 'Guardar cambios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': self.page_title,
            'form_title': self.form_title,
            'button_text': self.button_text,
        })
        return context

# Esta clase elimina el esquema entero del tenant por lo que es importante poner una advertencia y seguros antes de activarla.
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'clientes/confirmar_eliminacion.html' # Esta plantilla aún no existe
    success_url = reverse_lazy('clientes:lista_clientes') # Esta ruta aún no existe

    def delete(self, request, *args, **kwargs):
        cliente = self.get_object()
        messages.success(request, f'Cliente {cliente.nombre} eliminado correctamente.')
        return super().delete(request, *args, **kwargs)
