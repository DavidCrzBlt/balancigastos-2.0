from django.contrib import admin
from .models import Proyectos
# Register your models here.

class ProyectosAdmin(admin.ModelAdmin):
    list_display = [
        'proyecto',
        'clave_proyecto',
        'empresa',
        'estatus',
        'total',
        'iva'
    ]

    prepopulated_fields = {"slug": ["proyecto"]}

admin.site.register(Proyectos,ProyectosAdmin)