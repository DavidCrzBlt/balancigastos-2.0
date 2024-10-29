from django.test import TestCase
from .models import Ingresos, GastosEquipos, GastosGenerales, GastosManoObra, GastosMateriales, GastosSeguridad, GastosVehiculos
from proyectos.models import Proyectos
from equipos_y_vehiculos.models import Vehiculos
from decimal import Decimal
from django.core.exceptions import ValidationError
# Create your tests here.

class ProyectoActivoTestMixin:
    def setUp(self):
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

    # Métodos abstractos para sobreescribir
    def datos_adicionales_activo(self):
        raise NotImplementedError("Este método debe ser implementado en la subclase.")

    def datos_adicionales_inactivo(self):
        raise NotImplementedError("Este método debe ser implementado en la subclase.")
    
class IngresosModelTest(ProyectoActivoTestMixin, TestCase):
    Modelo = Ingresos
    
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

class GastosVehiculosModelTest(ProyectoActivoTestMixin, TestCase):
    Modelo = GastosVehiculos

    def setUp(self):
        super().setUp()  # Llama a la configuración base para crear los proyectos
        # Aquí creamos una instancia de Vehiculos para usarla en el test
        self.vehiculo = Vehiculos.objects.create(
            vehiculo = "Fiesta",
            marca = "Ford",
            color = "Rojo",
            placas = "MNA0912",
            combustible = "GASOLINE",
            valor_original = Decimal('100000')
        )
    
    def datos_adicionales_activo(self):
        return {
            "vehiculo": self.vehiculo ,# Asume que tienes que instanciar un Vehiculo antes
            "cantidad_combustible": 50,
            "monto": Decimal('1200.00'),
            "iva": Decimal('192.00'),
            "proveedor": "Proveedor A",
            "ubicacion": "Ciudad X",
            "conductor": "Conductor Y",
            "fecha": "2024-09-27"
        }

    def datos_adicionales_inactivo(self):
        return {
            "vehiculo": self.vehiculo, # Asume que tienes que instanciar un Vehiculo antes
            "cantidad_combustible": 40,
            "monto": Decimal('1000.00'),
            "iva": Decimal('160.00'),
            "proveedor": "Proveedor B",
            "ubicacion": "Ciudad Z",
            "conductor": "Conductor Z",
            "fecha": "2024-09-27"
        }

class GastosGeneralesModelTest(ProyectoActivoTestMixin, TestCase):
    Modelo = GastosGenerales
    
    def datos_adicionales_activo(self):
        return {
            "concepto": "Material Oficina",
            "comprador": "Persona A",
            "monto": Decimal('500.00'),
            "iva": Decimal('80.00'),
            "proveedor": "Proveedor C",
            "notas": "Nota adicional",
            "fecha": "2024-09-27"
        }
    
    def datos_adicionales_inactivo(self):
        return {
            "concepto": "Material Limpieza",
            "comprador": "Persona B",
            "monto": Decimal('300.00'),
            "iva": Decimal('48.00'),
            "proveedor": "Proveedor D",
            "notas": "Nota adicional",
            "fecha": "2024-09-27"
        }

class GastosMaterialesModelTest(ProyectoActivoTestMixin, TestCase):
    Modelo = GastosMateriales
    
    def datos_adicionales_activo(self):
        return {
            "concepto": "Material Oficina",
            "comprador": "Persona A",
            "monto": Decimal('500.00'),
            "iva": Decimal('80.00'),
            "proveedor": "Proveedor C",
            "descripcion": "Nota adicional",
            "fecha": "2024-09-27"
        }
    
    def datos_adicionales_inactivo(self):
        return {
            "concepto": "Material Limpieza",
            "comprador": "Persona B",
            "monto": Decimal('300.00'),
            "iva": Decimal('48.00'),
            "proveedor": "Proveedor D",
            "descripcion": "Nota adicional",
            "fecha": "2024-09-27"
        }

class GastosSeguridadModelTest(ProyectoActivoTestMixin, TestCase):
    Modelo = GastosSeguridad
    
    def datos_adicionales_activo(self):
        return {
            "concepto": "Material Oficina",
            "comprador": "Persona A",
            "monto": Decimal('500.00'),
            "iva": Decimal('80.00'),
            "proveedor": "Proveedor C",
            "descripcion": "Nota adicional",
            "fecha": "2024-09-27"
        }
    
    def datos_adicionales_inactivo(self):
        return {
            "concepto": "Material Limpieza",
            "comprador": "Persona B",
            "monto": Decimal('300.00'),
            "iva": Decimal('48.00'),
            "proveedor": "Proveedor D",
            "descripcion": "Nota adicional",
            "fecha": "2024-09-27"
        }

class GastosManoObraModelTest(ProyectoActivoTestMixin, TestCase):
    Modelo = GastosManoObra
    
    def datos_adicionales_activo(self):
        return {
            "nomina": Decimal('500.00'),
            "imss": Decimal('500.00'),
            "infonavit": Decimal('500.00'),
            "isn": Decimal('80.00'),
            "isr": Decimal('500.00'),
            "horas_extras": Decimal('500.00'),
            "monto":Decimal('500.00'),
            "fecha": "2024-09-27"
        }
    
    def datos_adicionales_inactivo(self):
        return {
            "nomina": Decimal('500.00'),
            "imss": Decimal('500.00'),
            "infonavit": Decimal('300.00'),
            "isn": Decimal('48.00'),
            "isr": Decimal('500.00'),
            "horas_extras": Decimal('500.00'),
            "monto":Decimal('500.00'),
            "fecha": "2024-09-27"
        }

class GastosEquiposModelTest(ProyectoActivoTestMixin, TestCase):
    Modelo = GastosEquipos
    
    def datos_adicionales_activo(self):
        return {
            "concepto": "Material Oficina",
            "comprador": "Persona A",
            "tiempo_renta": "RENTA_MENSUAL",
            "monto":Decimal('8000.00'),
            "iva": Decimal('80.00'),
            "proveedor": "Proveedor C",
            "descripcion": "Nota adicional",
            "fecha": "2024-09-27"
        }
    
    def datos_adicionales_inactivo(self):
        return {
            "concepto": "Material Limpieza",
            "comprador": "Persona B",
            "tiempo_renta": "RENTA_MENSUAL",
            "monto":Decimal('8000.00'),
            "iva": Decimal('48.00'),
            "proveedor": "Proveedor D",
            "descripcion": "Nota adicional",
            "fecha": "2024-09-27"
        }
