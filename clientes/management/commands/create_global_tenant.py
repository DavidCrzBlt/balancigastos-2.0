# management/commands/create_global_tenant.py

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.sites.models import Site
from clientes.models import Cliente, DominioCliente 

import os
from dotenv import load_dotenv

class Command(BaseCommand):
    help = 'Create the global tenant'

    def handle(self, *args, **kwargs):
        # Global tenant details
        tenant_name = 'Main Tenant'
        schema_name = 'public'
        tenant_domain = os.getenv('MAIN_DOMAIN')

        try:
            with transaction.atomic():
                # Create the tenant
                tenant = Cliente(schema_name=schema_name,nombre=tenant_name, dominio=tenant_domain)
                tenant.save()

                # Create the associated domain for the tenant
                dominio_cliente = DominioCliente()
                dominio_cliente.domain = tenant_domain
                dominio_cliente.tenant = tenant
                dominio_cliente.is_primary = True 
                dominio_cliente.save()

                # Crear un nuevo sitio para localhost
                site = Site(id=2,domain=tenant_domain, name=tenant_name)
                site.save()

                self.stdout.write(self.style.SUCCESS('Successfully created global tenant: %s' % tenant_name))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Error creating tenant: %s' % e))
