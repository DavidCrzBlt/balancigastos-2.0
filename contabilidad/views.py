from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Sum, ProtectedError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy

from decimal import Decimal

from .models import Ingresos, Gasto, CategoriaGasto, NominaEmpleado, Lote
from .forms import GastoForm, CategoriaGastoForm, NominaEmpleadoForm, IngresosForm
from .utils import recalcular_totales_proyecto
from .mixins import ProyectoOperacionMixin, ProyectoDeleteMixin

from proyectos.models import Proyectos

# Create your views here.

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
    
class ActualizarIngresoView(LoginRequiredMixin, ProyectoOperacionMixin, UpdateView):
    model = Ingresos
    form_class = IngresosForm
    template_name = "form_template.html"

    def get_success_url(self):
        return reverse('contabilidad:ingresos', kwargs={'slug': self.proyecto.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': f'Actualizar ingreso {self.proyecto}',
            'button_text': 'Actualizar ingreso',
            'page_title': f'Actualizar ingreso {self.proyecto}',
            'proyecto': self.proyecto,
            'active_tab': 'ingresos',
            'mostrar_tabs': True,
        })
        return context

class EliminarIngresoView(LoginRequiredMixin, ProyectoDeleteMixin, DeleteView):
    model = Ingresos
    template_name = "confirm_delete.html"
    list_url_name = "contabilidad:ingresos"
    success_message = "Ingreso eliminado correctamente"
    
    
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
    
class ActualizarGastoView(LoginRequiredMixin, ProyectoOperacionMixin, UpdateView):
    model = Gasto
    form_class = GastoForm
    template_name = "form_template.html"

    def get_success_url(self):
        return reverse('contabilidad:gastos', kwargs={'slug': self.proyecto.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': f'Actualizar gasto {self.proyecto}',
            'button_text': 'Actualizar gasto',
            'page_title': f'Actualizar gasto {self.proyecto}',
            'proyecto': self.proyecto,
            'active_tab': 'gastos',
            'mostrar_tabs': True,
        })
        return context

class EliminarGastoView(LoginRequiredMixin, ProyectoDeleteMixin, DeleteView):
    model = Gasto
    template_name = "confirm_delete.html"
    list_url_name = "contabilidad:gastos"
    success_message = "Gasto eliminado correctamente"


class CrearNominaView(LoginRequiredMixin,CreateView):
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
        recalcular_totales_proyecto(self.proyecto)

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
    
class ActualizarNominaView(LoginRequiredMixin, UpdateView):
    model = NominaEmpleado
    form_class = NominaEmpleadoForm
    template_name = 'form_template.html'

    def dispatch(self, request, *args, **kwargs):
        self.nomina = self.get_object()
        self.proyecto = self.nomina.proyecto
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        nomina = form.save()

        # Actualizar gasto asociado
        try:
            gasto = Gasto.objects.get(lote=nomina.lote)
            gasto.monto = nomina.total
            gasto.fecha = nomina.fecha
            gasto.descripcion = f"Nómina para {nomina.empleado} en lote {nomina.lote.id}"
            gasto.save()
        except Gasto.DoesNotExist:
            print(f"Gasto asociado a lote {nomina.lote.id} no encontrado.")

        recalcular_totales_proyecto(self.proyecto)
        messages.success(self.request, "Nómina actualizada correctamente.")
        return redirect('contabilidad:nominas', slug=self.proyecto.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': f'Actualizar nómina {self.proyecto}',
            'button_text': 'Guardar cambios',
            'page_title': f'Editar nómina {self.proyecto}',
            'proyecto': self.proyecto,
            'active_tab': 'nóminas',
            'mostrar_tabs': True,
        })
        return context
    
class EliminarNominaView(LoginRequiredMixin, DeleteView):
    model = NominaEmpleado

    def dispatch(self, request, *args, **kwargs):
        self.nomina = self.get_object()
        self.proyecto = self.nomina.proyecto
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        nomina = self.get_object()
        lote = nomina.lote

        nomina.delete()

        # Eliminar gasto asociado
        try:
            gasto = Gasto.objects.get(lote=lote)
            gasto.delete()
        except Gasto.DoesNotExist:
            print(f"Gasto no encontrado para lote {lote.id}")

        # Eliminar lote (opcional, solo si se elimina toda la nómina ligada a él)
        if not NominaEmpleado.objects.filter(lote=lote).exists():
            lote.delete()

        recalcular_totales_proyecto(self.proyecto.id)
        messages.success(request, "Nómina eliminada correctamente.")
        return redirect('contabilidad:nominas', slug=self.proyecto.slug)

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


class ListaCategoriasGastoView(LoginRequiredMixin, ListView):
    model = CategoriaGasto
    template_name = 'contabilidad/lista_categorias.html'
    context_object_name = 'categorias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Categorías de gasto'
        return context
    
class ActualizarCategoriaGastoView(LoginRequiredMixin, UpdateView):
    model = CategoriaGasto
    form_class = CategoriaGastoForm
    template_name = 'form_template.html'

    def get_success_url(self):
        return reverse('contabilidad:categorias_gasto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': 'Editar categoría de gasto',
            'button_text': 'Guardar cambios',
            'page_title': 'Editar categoría',
        })
        return context

class EliminarCategoriaGastoView(LoginRequiredMixin, DeleteView):
    model = CategoriaGasto
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('contabilidad:categorias_gasto')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'cancel_url':reverse_lazy('contabilidad:categorias_gasto'),
        })
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, f"No puedes eliminar la categoría '{self.object.nombre}' porque está asociada a uno o más gastos.")
            return redirect(self.get_success_url())

