from empleados.models import Salario as SalarioViejo, Lote as LoteViejo
from contabilidad.models import Lote, NominaEmpleado
from django.utils import timezone

def migrar_nominas():
    for s in SalarioViejo.objects.all():
        # Crear lote si no existe en contabilidad
        lote_nuevo, _ = Lote.objects.get_or_create(
            proyecto=s.proyecto,
            defaults={'descripcion': f"Lote importado desde empleados {s.lote}"}
        )

        NominaEmpleado.objects.create(
            empleado=s.empleado,
            proyecto=s.proyecto,
            lote=lote_nuevo,
            fecha=timezone.now(),  # si tienes fecha original, úsala
            salario_base=s.salario,
            imss=s.imss,
            infonavit=s.infonavit,
            isr=s.isr,
            horas_extras=s.horas_extras
        )
