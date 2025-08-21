from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from empleados.models import Empleados, Asistencias
from empleados.forms import EmpleadosForm, AsistenciaForm
from proyectos.models import Proyectos

from core.views import FormularioGenericoView

# Create your views here.

# ------------------------------ Empleados ------------------------------

class ListaEmpleadosView(LoginRequiredMixin, ListView):
    model = Empleados
    template_name = 'empleados/empleados.html'
    context_object_name = 'empleados'


class CrearEmpleadoView(LoginRequiredMixin, CreateView):
    model = Empleados
    form_class = EmpleadosForm
    template_name = 'form_template.html'

    def get_success_url(self):
        return reverse('empleados:empleados')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': 'Agregar empleado',
            'button_text': 'Crear empleado',
            'page_title': 'Nuevo empleado',
        })
        return context


class ActualizarEmpleadoView(LoginRequiredMixin, UpdateView):
    model = Empleados
    form_class = EmpleadosForm
    template_name = 'form_template.html'

    def get_success_url(self):
        return reverse('empleados:empleados')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': 'Editar empleado',
            'button_text': 'Actualizar empleado',
            'page_title': 'Editar empleado',
        })
        return context


class EliminarEmpleadoView(LoginRequiredMixin, DeleteView):
    model = Empleados
    template_name = 'confirm_delete.html'
    def get_success_url(self):
        # No poder eliminar empleados, solo darlos de baja si tienen asistencias asignadas
        messages.success(self.request, "Empleado eliminado exitosamente.")
        return reverse('empleados:empleados')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'cancel_url':reverse_lazy('empleados:empleados'),
        })
        return context


# ------------------------------ Asistencias ------------------------------

class ListaAsistenciasView(LoginRequiredMixin, ListView):
    model = Asistencias
    template_name = 'empleados/asistencias.html'
    context_object_name = 'asistencias'

    def get_queryset(self):
        self.proyecto = get_object_or_404(Proyectos, slug=self.kwargs['slug'])
        return Asistencias.objects.filter(proyecto=self.proyecto)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proyecto'] = self.proyecto
        return context


class CrearAsistenciaView(LoginRequiredMixin, CreateView):
    model = Asistencias
    form_class = AsistenciaForm
    template_name = 'form_template.html'

    def dispatch(self, request, *args, **kwargs):
        self.proyecto = get_object_or_404(Proyectos, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.proyecto = self.proyecto
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('empleados:asistencias', kwargs={'slug': self.proyecto.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': f'Registrar asistencia para {self.proyecto}',
            'button_text': 'Guardar asistencia',
            'page_title': f'Nueva asistencia para {self.proyecto}',
            'proyecto': self.proyecto,
            'active_tab':'asistencias',
            'mostrar_tabs':True,
        })
        return context


class ActualizarAsistenciaView(LoginRequiredMixin, UpdateView):
    model = Asistencias
    form_class = AsistenciaForm
    template_name = 'form_template.html'

    def dispatch(self, request, *args, **kwargs):
        self.proyecto = get_object_or_404(Proyectos, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('empleados:asistencias', kwargs={'slug': self.proyecto.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_title': f'Actualizar asistencia para {self.proyecto}',
            'button_text': 'Actualizar asistencia',
            'page_title': f'Actualizar asistencia para {self.proyecto}',
            'proyecto': self.proyecto,
            'active_tab':'asistencias',
            'mostrar_tabs':True,
        })
        return context


class EliminarAsistenciaView(LoginRequiredMixin, DeleteView):
    model = Asistencias
    template_name = 'confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        self.proyecto = get_object_or_404(Proyectos, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "Asistencia eliminada exitosamente.")
        return reverse('empleados:asistencias', kwargs={'slug': self.proyecto.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'cancel_url':reverse_lazy('empleados:asistencias'),
        })
        return context
