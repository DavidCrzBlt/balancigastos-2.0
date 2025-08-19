from django.shortcuts import render, redirect, get_object_or_404
from .forms import GastosVehiculosForm, GastosGeneralesForm, GastosMaterialesForm, GastosManoObraForm, GastosSeguridadForm, GastosEquiposForm, IngresosForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import GastosVehiculos, GastosGenerales, GastosMateriales, GastosManoObra, GastosEquipos, GastosSeguridad, Ingresos
from proyectos.models import Proyectos
from empleados.models import Salario
from django.db.models import Sum, F
from django.db.models.functions import Coalesce, ExtractWeek, ExtractYear
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal
from django.contrib import messages
from .models import Gasto, CategoriaGasto
from .forms import GastoForm, CategoriaGastoForm, NominaEmpleadoForm
from contabilidad.utils import calcular_iva, recalcular_totales_proyecto
from contabilidad.mixins import ProyectoOperacionMixin
from django.urls import reverse

import pandas as pd


from .models import NominaEmpleado, Lote, Gasto, CategoriaGasto

# Create your views here.

### Vistas de detalle de proyecto ------------------------------------------- ###
### Funciones genéricas para registro, edición y eliminación de instancias--- ###
### Funciones de registro y edición de instancias por tipo de gasto o ingreso ###
### Funciones de eliminación de instancias ---------------------------------- ###

### ------------------------------------------------------------------------- ###
### ------------------------------------------------------------------------- ###
# Se muestran todas las vistas de los detalles del proyecto
### ------------------------------------------------------------------------- ###
### ------------------------------------------------------------------------- ###


class ListaGastosView(LoginRequiredMixin, ListView):
    model = Gasto
    template_name = 'contabilidad/gastos.html'
    context_object_name = 'gastos'

    def get_queryset(self):
        proyecto = Proyectos.objects.get(slug=self.kwargs['slug'])
        return Gasto.objects.filter(proyecto=proyecto).order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        proyecto = Proyectos.objects.get(slug=slug)

        context.update({
            'page_title': f'Lista de gastos {proyecto}',
            'proyecto': proyecto,
            'active_tab': 'gastos',
            'mostrar_tabs': True,
        })
        return context


class ListaCategoriasGastoView(LoginRequiredMixin, ListView):
    model = CategoriaGasto
    template_name = 'contabilidad/lista_categorias.html'
    context_object_name = 'categorias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Categorías de gasto'
        return context
    
class ListaNominasView(LoginRequiredMixin, ListView):
    model = NominaEmpleado
    template_name = 'contabilidad/nominas_list.html'
    context_object_name = 'nominas'

    def get_queryset(self):
        proyecto = Proyectos.objects.get(slug=self.kwargs['slug'])
        return NominaEmpleado.objects.filter(proyecto=proyecto).order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        proyecto = Proyectos.objects.get(slug=slug)
        context.update({
            'page_title': f'Lista de nóminas {proyecto}',
            'proyecto': proyecto,
            'active_tab': 'nóminas',
            'mostrar_tabs': True,
        })
        return context


class IngresosListView(LoginRequiredMixin,ListView):
    model = Ingresos
    template_name = "contabilidad/ingresos.html"

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        proyecto = Proyectos.objects.get(slug=slug)
        return Ingresos.objects.filter(proyecto=proyecto)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        proyecto = Proyectos.objects.get(slug=slug)

        # Calculate total monto using aggregate
        total_monto = Ingresos.objects.filter(proyecto=proyecto).aggregate(total=Sum('monto'))['total'] or 0

        # Calculate total iva using aggregate
        total_iva = Ingresos.objects.filter(proyecto=proyecto).aggregate(total=Sum('iva'))['total'] or 0

        # Add the total to the context
        context.update({
            'page_title': f'Lista de ingresos {proyecto}',
            'proyecto': proyecto,
            'total_monto': total_monto,
            'total_iva': total_iva,
            'active_tab': 'ingresos',
            'mostrar_tabs': True,
        })
        return context 
    
### ------------------------------------------------------------------------- ###
### ------------------------------------------------------------------------- ###

@login_required
def eliminar_operaciones_generico(request,slug,modelo,instancia_id,redirect_url):
    # Obtener el proyecto
    proyecto = get_object_or_404(Proyectos, slug=slug)

    if proyecto.estatus == True:

        # Buscar el movimiento por ID
        movimiento = get_object_or_404(modelo, id=instancia_id, proyecto=proyecto)

        # Eliminar el movimiento
        movimiento.delete()

        # Actualizar el valor neto del proyecto (suma o resta según la categoría)
        recalcular_totales_proyecto(proyecto.id)

        # Mostrar un mensaje de éxito
        messages.success(request, 'El gasto ha sido eliminado exitosamente.')

        # Redirigir a la lista de gastos o a la página que prefieras
        return redirect(redirect_url, slug=slug)
    else:
        # Mostrar un mensaje de advertencia
        messages.error(request, 'No se pueden hacer cambios a un proyecto inactivo.')
        # Redirigir a página de error
        return redirect(redirect_url,slug=slug)

### ------------------------------------------------------------------------- ###
### ------------------------------------------------------------------------- ###
# A partir de aquí se registran los gastos e ingresos
### ------------------------------------------------------------------------- ###
### ------------------------------------------------------------------------- ###

class CrearIngresoView(LoginRequiredMixin, ProyectoOperacionMixin, CreateView):
    model = Ingresos
    form_class = IngresosForm
    template_name = 'form_template.html'

    def get_success_url(self):
        return reverse('contabilidad:ingresos', kwargs={'slug': self.proyecto.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'form_title': f'Registrar ingreso {self.proyecto}',
            'button_text': 'Guardar ingreso',
            'page_title': f'Registro de ingresos {self.proyecto}',
            'proyecto': self.proyecto,
            'active_tab': 'ingresos',
            'mostrar_tabs': True,
        })
        return context


class CrearGastoView(LoginRequiredMixin, ProyectoOperacionMixin, CreateView):
    model = Gasto
    form_class = GastoForm
    template_name = 'form_template.html'

    def get_success_url(self):
        return reverse('contabilidad:gastos', kwargs={'slug': self.proyecto.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'form_title': f'Registrar gasto {self.proyecto}',
            'button_text': 'Guardar gasto',
            'page_title': f'Registro de gastos {self.proyecto}',
            'proyecto': self.proyecto,
            'active_tab': 'gastos',
            'mostrar_tabs': True,
        })

        return context
    
class CrearNominaView(CreateView):
    model = NominaEmpleado
    form_class = NominaEmpleadoForm
    template_name = 'form_template.html'

    def dispatch(self, request, *args, **kwargs):
        self.proyecto = get_object_or_404(Proyectos, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Crear un lote automáticamente
        lote = Lote.objects.create(proyecto=self.proyecto)

        nomina = form.save(commit=False)
        nomina.lote = lote
        nomina.proyecto = self.proyecto
        nomina.save()

        # Crear gasto asociado
        categoria = CategoriaGasto.objects.get(nombre="Mano de Obra")
        Gasto.objects.create(
            proyecto=self.proyecto,
            categoria=categoria,
            concepto = f"Mano de Obra/Lote: {lote}",
            monto=nomina.total,
            iva=Decimal('0.00'),
            fecha=nomina.fecha,
            descripcion=f"Nómina para {nomina.empleado} en lote {lote.id}",
            lote=lote
        )

        # Recalcular totales del proyecto
        recalcular_totales_proyecto(self.proyecto.id)

        messages.success(self.request, "Nómina registrada exitosamente.")
        return redirect('contabilidad:nominas', slug=self.proyecto.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': f'Registrar nómina {self.proyecto}',
            'button_text': 'Guardar nómina',
            'page_title': f'Registro de nóminas {self.proyecto}',
            'proyecto': self.proyecto,
            'active_tab': 'nóminas',
            'mostrar_tabs': True,
        })
        return context


class CrearCategoriaGastoView(LoginRequiredMixin, CreateView):
    model = CategoriaGasto
    form_class = CategoriaGastoForm
    template_name = 'form_template.html'
    
    def get_success_url(self):
        return reverse('contabilidad:categorias_gasto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': 'Agregar categoría de gasto',
            'button_text': 'Crear categoría',
            'page_title': 'Nueva categoría',
        })
        return context


### ------------------------------------------------------------------------- ###
### ------------------------------------------------------------------------- ###
# A partir de aquí se eliminan instancias de gastos o ingresos
### ------------------------------------------------------------------------- ###
### ------------------------------------------------------------------------- ###

@login_required
def eliminar_ingresos(request, slug, gasto_id):
    return eliminar_operaciones_generico(
            request=request,
            slug=slug,
            modelo=Ingresos,
            instancia_id=gasto_id, 
            redirect_url='contabilidad:ingresos',  # URL a la que redirigir
        )