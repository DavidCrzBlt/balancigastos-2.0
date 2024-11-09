from django.test import TestCase
from django.test import TestCase
from django_tenants.utils import tenant_context
from clientes.models import Cliente
from proyectos.models import Proyectos  

class TenantTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Crea un tenant de prueba
        cls.tenant = Cliente.objects.create(
            dominio='prueba.localhost',
            schema_name='prueba',
            # Rellena los demás campos requeridos por el modelo
        )
        cls.tenant.save()

    def setUp(self):
        # Esto asegura que cada prueba se ejecute en el contexto del inquilino
        self.tenant_context = tenant_context(self.tenant)
        self.tenant_context.__enter__()

    def tearDown(self):
        # Sal del contexto al final de cada prueba
        self.tenant_context.__exit__(None, None, None)

    def test_proyecto_creation(self):
        # Ejemplo de prueba en el contexto del inquilino
        proyecto = Proyectos.objects.create(
            proyecto = "Proyecto de Prueba",
            clave_proyecto = "Descripción del proyecto de prueba",
            # Agrega otros campos necesarios
        )
        self.assertEqual(proyecto.proyecto, "Proyecto de Prueba")
