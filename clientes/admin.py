from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from clientes.models import Cliente

@admin.register(Cliente)
class ClienteAdmin(TenantAdminMixin, admin.ModelAdmin):
        list_display = ('nombre', 'dominio')