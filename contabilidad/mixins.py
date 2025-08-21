from .utils import calcular_iva, recalcular_totales_proyecto

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
