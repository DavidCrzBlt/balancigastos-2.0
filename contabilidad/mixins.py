from .utils import calcular_iva, recalcular_totales_proyecto

# mixins.py
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.contrib import messages

class ProyectoDeleteMixin:
    """
    Mixin para DeleteView que:
    - Obtiene self.proyecto a partir de slug
    - Garantiza ownership del objeto (obj.proyecto_id == self.proyecto.id)
    - Recalcula totales después del borrado
    - Resuelve cancel_url y success_url
    Requiere: definir `list_url_name` (por ej. 'contabilidad:ingresos')
              opcional: `success_message`
    """
    list_url_name = None
    success_message = None

    def dispatch(self, request, *args, **kwargs):
        from proyectos.models import Proyectos
        self.proyecto = get_object_or_404(Proyectos, slug=kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if getattr(obj, "proyecto_id", None) != self.proyecto.id:
            raise Http404("El objeto no pertenece a este proyecto.")
        return obj

    def delete(self, request, *args, **kwargs):
        # Guardar referencias ANTES de borrar
        self.object = self.get_object()
        self._success_slug = self.proyecto.slug
        proyecto_id = self.proyecto.id

        # Borrado normal (crea el redirect response)
        response = super().delete(request, *args, **kwargs)

        # Hook post-delete: recalcular
        try:
            self.after_delete(proyecto_id)
            if self.success_message:
                messages.success(request, self.success_message)
        except Exception as e:
            # En producción, usa logger.exception(...)
            print(f"Error en after_delete: {e}")

        return response

    # Hook para acciones post-borrado (sobrescribible si quieres)
    def after_delete(self, proyecto_id):
        from contabilidad.utils import recalcular_totales_proyecto  # ajusta import
        recalcular_totales_proyecto(proyecto_id)

    def get_success_url(self):
        if not self.list_url_name:
            raise ValueError("Define list_url_name en la vista hija.")
        return reverse(self.list_url_name, kwargs={"slug": self.proyecto.slug})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if not self.list_url_name:
            raise ValueError("Define list_url_name en la vista hija.")
        ctx.update({
            "cancel_url": reverse_lazy(self.list_url_name, kwargs={"slug": self.proyecto.slug}),
            # opcionales, por si tu template genérico los usa:
            "proyecto": self.proyecto,
        })
        return ctx


class ProyectoOperacionMixin:
    proyecto = None  # Se asigna en dispatch

    def dispatch(self, request, *args, **kwargs):
        from proyectos.models import Proyectos  # Import aquí para evitar dependencias circulares
        self.proyecto = Proyectos.objects.get(slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.proyecto = self.proyecto

        # Calcular IVA si el modelo tiene el campo
        if hasattr(form.instance, 'iva') and hasattr(form.instance, 'monto'):
            form.instance.iva = calcular_iva(form.instance.monto)

        response = super().form_valid(form)

        try:
            resultado = recalcular_totales_proyecto(self.proyecto.id)
            print(f"Totales recalculados para {self.proyecto}: {resultado}")
        except Exception as e:
            print(f"Error al recalcular totales del proyecto {self.proyecto}: {e}")

        return response
