from django.test import TestCase
from .models import Ingresos, GastosEquipos, GastosGenerales, GastosManoObra, GastosMateriales, GastosSeguridad, GastosVehiculos
from proyectos.models import Proyectos
from equipos_y_vehiculos.models import Vehiculos
from decimal import Decimal
from django.core.exceptions import ValidationError
from clientes.models import Cliente


class TenantTestCase(TestCase):
    def setUp(self):
        # Creamos un tenant para utilizar en los tests
        self.tenant = Cliente.objects.create(
            nombre="Tenant Test",
            dominio="tenanttest.local",
            schema_name="tenant_test"
        )
        self.tenant.save()
        # Si tu configuración de tenantes requiere algún cambio de esquema, debes hacerlo aquí.
        self.tenant.activate()  # Activa el esquema del tenant para el test

    def tearDown(self):
        self.tenant.delete()  # Limpia el tenant después del test
        self.tenant.deactivate()

class ProyectoActivoTestMixin(TenantTestCase):
    def setUp(self):
        super().setUp()  
        # Creamos un proyecto activo y uno inactivo para usar en los tests
        self.proyecto_activo = Proyectos.objects.create(
            proyecto="Proyecto Activo",
            clave_proyecto="PA001",
            empresa="Empresa Activa",
            estatus=True,  # Proyecto activo
            total=Decimal('10000.00'),
            iva=Decimal('1600.00')
        )

        self.proyecto_inactivo = Proyectos.objects.create(
            proyecto="Proyecto Inactivo",
            clave_proyecto="PI001",
            empresa="Empresa Inactiva",
            estatus=False,  # Proyecto inactivo
            total=Decimal('5000.00'),
            iva=Decimal('800.00')
        )

    # Métodos abstractos para sobreescribir
    def datos_adicionales_activo(self):
        raise NotImplementedError("Este método debe ser implementado en la subclase.")

    def datos_adicionales_inactivo(self):
        raise NotImplementedError("Este método debe ser implementado en la subclase.")


class IngresosModelTest(ProyectoActivoTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.Modelo = Ingresos
    
    def datos_adicionales_activo(self):
        return {
            "concepto": "Venta de servicios",
            "monto": Decimal('500.00'),
            "iva": Decimal('80.00'),
            "referencia": "REF123",
            "fecha": "2024-09-27"
        }
    
    def datos_adicionales_inactivo(self):
        return {
            "concepto": "Venta de productos",
            "monto": Decimal('1000.00'),
            "iva": Decimal('160.00'),
            "referencia": "REF124",
            "fecha": "2024-09-27"
        }
    
    def test_crear_registro_con_proyecto_activo(self):
        modelo = self.Modelo.objects.create(
            proyecto=self.proyecto_activo,
            **self.datos_adicionales_activo()
        )
        self.assertEqual(modelo.proyecto.estatus, True)

    def test_no_crear_registro_con_proyecto_inactivo(self):
        with self.assertRaises(ValidationError):
            modelo = self.Modelo.objects.create(
                proyecto=self.proyecto_inactivo,
                **self.datos_adicionales_inactivo()
            )
            if not modelo.proyecto.estatus:
                raise ValidationError("No se puede registrar en un proyecto inactivo")
