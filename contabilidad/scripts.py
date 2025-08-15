from django_tenants.utils import schema_context
from clientes.models import Cliente  # Modelo tenant
from contabilidad.models import CategoriaGasto, Gasto, Lote, NominaEmpleado
from empleados.models import Empleados, Salario
from decimal import Decimal
from django.utils import timezone

# Modelos antiguos
from contabilidad.models import (
    GastosVehiculos, GastosGenerales, GastosMateriales,
    GastosSeguridad, GastosEquipos, GastosManoObra
)


def migrar_todo():
    print("=== Iniciando migración de datos en todos los tenants ===")

    for tenant in Cliente.objects.exclude(schema_name='public'):
        with schema_context(tenant.schema_name):
            print(f"\n--- Migrando en esquema: {tenant.schema_name} ---")

            try:
                categorias = {
                    "Vehículos": CategoriaGasto.objects.get(nombre="Vehículos"),
                    "Generales": CategoriaGasto.objects.get(nombre="Generales"),
                    "Materiales": CategoriaGasto.objects.get(nombre="Materiales"),
                    "Seguridad": CategoriaGasto.objects.get(nombre="Seguridad"),
                    "Equipos": CategoriaGasto.objects.get(nombre="Equipos"),
                    "Mano de Obra": CategoriaGasto.objects.get(nombre="Mano de Obra"),
                }
            except CategoriaGasto.DoesNotExist:
                print(f"❌ Categorías no encontradas en {tenant.schema_name}. Saltando tenant...")
                continue

            total_gastos = 0
            total_nominas = 0

            # Migrar GastosVehiculos
            for g in GastosVehiculos.objects.all():
                Gasto.objects.create(
                    proyecto=g.proyecto,
                    categoria=categorias["Vehículos"],
                    monto=g.monto,
                    iva=g.iva,
                    fecha=g.fecha,
                    descripcion=f"Proveedor: {g.proveedor} | Ubicación: {g.ubicacion} | Conductor: {g.conductor}"
                )
                total_gastos += 1

            # Migrar GastosGenerales
            for g in GastosGenerales.objects.all():
                Gasto.objects.create(
                    proyecto=g.proyecto,
                    categoria=categorias["Generales"],
                    monto=g.monto,
                    iva=g.iva,
                    fecha=g.fecha,
                    descripcion=f"Proveedor: {g.proveedor} | Comprador: {g.comprador} | Concepto: {g.concepto}"
                )
                total_gastos += 1

            # Migrar GastosMateriales
            for g in GastosMateriales.objects.all():
                Gasto.objects.create(
                    proyecto=g.proyecto,
                    categoria=categorias["Materiales"],
                    monto=g.monto,
                    iva=g.iva,
                    fecha=g.fecha,
                    descripcion=f"Proveedor: {g.proveedor} | Comprador: {g.comprador} | Concepto: {g.concepto}"
                )
                total_gastos += 1

            # Migrar GastosSeguridad
            for g in GastosSeguridad.objects.all():
                Gasto.objects.create(
                    proyecto=g.proyecto,
                    categoria=categorias["Seguridad"],
                    monto=g.monto,
                    iva=g.iva,
                    fecha=g.fecha,
                    descripcion=f"Proveedor: {g.proveedor} | Comprador: {g.comprador} | Concepto: {g.concepto}"
                )
                total_gastos += 1

            # Migrar GastosEquipos
            for g in GastosEquipos.objects.all():
                Gasto.objects.create(
                    proyecto=g.proyecto,
                    categoria=categorias["Equipos"],
                    monto=g.monto,
                    iva=g.iva,
                    fecha=g.fecha,
                    descripcion=f"Proveedor: {g.proveedor} | Comprador: {g.comprador} | Concepto: {g.concepto} | Tiempo renta: {g.tiempo_renta}"
                )
                total_gastos += 1

            # Migrar Mano de Obra
            for g in GastosManoObra.objects.all():
                lote = Lote.objects.create(
                    proyecto=g.proyecto,
                    descripcion=f"Lote migrado desde GastosManoObra #{g.lote}"
                )
                Gasto.objects.create(
                    proyecto=g.proyecto,
                    categoria=categorias["Mano de Obra"],
                    monto=g.monto,
                    iva=Decimal("0.00"),
                    fecha=g.fecha,
                    lote=lote,
                    descripcion="Gasto de mano de obra agregado"
                )
                total_gastos += 1

            # Migrar Nóminas individuales
            for s in Salario.objects.all():
                lote, _ = Lote.objects.get_or_create(
                    proyecto=s.proyecto,
                    descripcion=f"Lote migrado desde Salario (#{s.lote})"
                )
                NominaEmpleado.objects.create(
                    empleado=s.empleado,
                    proyecto=s.proyecto,
                    lote=lote,
                    fecha=timezone.now(),
                    salario_base=s.salario,
                    imss=s.imss,
                    infonavit=s.infonavit,
                    isr=s.isr,
                    isn=Decimal("0.00"),
                    horas_extras=s.horas_extras
                )
                total_nominas += 1

            print(f"✅ {total_gastos} gastos y {total_nominas} nóminas migrados en {tenant.schema_name}")

    print("\n=== Migración completada en todos los tenants ===")
