from django.contrib import admin
from .models import Ingresos, GastosEquipos, GastosGenerales, GastosManoObra, GastosMateriales, GastosSeguridad, GastosVehiculos
# Register your models here.

class IngresosAdmin(admin.ModelAdmin):
    list_display = [
        'proyecto',
        'concepto',
        'monto',
        'iva',
        'referencia',
        'fecha'
    ]

class GastosEquiposAdmin(admin.ModelAdmin):
    list_display = [
        'proyecto',
        'concepto',
        'comprador',
        'tiempo_renta',
        'monto',
        'iva',
        'descripcion',
        'proveedor',
        'fecha'
    ]

class GastosGeneralesAdmin(admin.ModelAdmin):
    list_display = [
        'proyecto',
        'concepto',
        'comprador',
        'monto',
        'iva',
        'notas',
        'proveedor',
        'fecha'
    ]

class GastosMaterialesAdmin(admin.ModelAdmin):
    list_display = [
        'proyecto',
        'concepto',
        'comprador',
        'monto',
        'iva',
        'descripcion',
        'proveedor',
        'fecha'
    ]

class GastosSeguridadAdmin(admin.ModelAdmin):
    list_display = [
        'proyecto',
        'concepto',
        'comprador',
        'monto',
        'iva',
        'descripcion',
        'proveedor',
        'fecha'
    ]

class GastosVehiculosAdmin(admin.ModelAdmin):
    list_display = [
        'proyecto',
        'vehiculo',
        'cantidad_combustible',
        'conductor',
        'monto',
        'iva',
        'ubicacion',
        'proveedor',
        'fecha'
    ]

class GastosManoObraAdmin(admin.ModelAdmin):
    list_display = [
        'proyecto',
        'nomina',
        'imss',
        'infonavit',
        'isn',
        'isr',
        'horas_extras',
        'monto',
        'lote',
        'fecha'
    ]

admin.site.register(Ingresos,IngresosAdmin)
admin.site.register(GastosGenerales,GastosGeneralesAdmin)
admin.site.register(GastosMateriales,GastosMaterialesAdmin)
admin.site.register(GastosVehiculos,GastosVehiculosAdmin)
admin.site.register(GastosSeguridad,GastosSeguridadAdmin)
admin.site.register(GastosEquipos,GastosEquiposAdmin)
admin.site.register(GastosManoObra,GastosManoObraAdmin)