from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

# Create your models here.

class Cliente(TenantMixin):
    nombre = models.CharField(max_length=100)
    dominio = models.CharField(max_length=100, unique=True)
    esquema_creado = models.DateTimeField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

class DominioCliente(DomainMixin):
    pass