from decimal import Decimal
from django.db.models import Sum
from django.db.models.functions import Coalesce
from .models import Ingresos, Gasto, CategoriaGasto
from proyectos.models import Proyectos


def calcular_iva(monto):
    return monto * Decimal('0.16')


def recalcular_totales_proyecto(proyecto):
    proyecto = Proyectos.objects.get(proyecto=proyecto)

    # === INGRESOS ===
    ingresos_result = Ingresos.objects.filter(proyecto=proyecto).aggregate(
        total_ingresos=Coalesce(Sum('monto'), Decimal('0.00')),
        total_iva=Coalesce(Sum('iva'), Decimal('0.00'))
    )
    total_ingresos = ingresos_result['total_ingresos']
    total_iva_ingresos = ingresos_result['total_iva']

    # === GASTOS DINÁMICOS ===
    total_gastos = Decimal('0.00')
    total_iva_gastos = Decimal('0.00')

    # Diccionario para detalle por categoría
    detalle_gastos = {}

    categorias = CategoriaGasto.objects.all()

    for cat in categorias:
        gastos_agg = Gasto.objects.filter(proyecto=proyecto, categoria=cat).aggregate(
            total_cat=Coalesce(Sum('monto'), Decimal('0.00')),
            total_iva_cat=Coalesce(Sum('iva'), Decimal('0.00'))
        )

        detalle_gastos[cat.nombre] = {
            'monto': gastos_agg['total_cat'],
            'iva': gastos_agg['total_iva_cat'],
        }

        total_gastos += gastos_agg['total_cat']
        total_iva_gastos += gastos_agg['total_iva_cat']

    # === Actualizar proyecto ===
    proyecto.total = total_ingresos - total_gastos
    proyecto.iva = total_iva_ingresos - total_iva_gastos
    proyecto.save()

    return {
        'total_ingresos': total_ingresos,
        'total_iva_ingresos': total_iva_ingresos,
        'total_gastos': total_gastos,
        'total_iva_gastos': total_iva_gastos,
        'detalle_gastos': detalle_gastos,
        'total_neto': proyecto.total,
        'iva_neto': proyecto.iva
    }


def obtener_totales_por_categoria(proyecto):
    """
    Devuelve un diccionario con los totales de monto e IVA por cada categoría de gasto
    para el proyecto proporcionado.
    """
    categorias = CategoriaGasto.objects.all()
    resultados = {}

    for cat in categorias:
        agregados = Gasto.objects.filter(proyecto=proyecto, categoria=cat).aggregate(
            total_monto=Sum('monto') or Decimal('0.00'),
            total_iva=Sum('iva') or Decimal('0.00')
        )

        resultados[cat.nombre] = {
            'monto': agregados['total_monto'] or Decimal('0.00'),
            'iva': agregados['total_iva'] or Decimal('0.00')
        }

    return resultados
