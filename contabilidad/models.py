from django.db import models
from proyectos.models import Proyectos
from equipos_y_vehiculos.models import Vehiculos
from django.utils import timezone
from decimal import Decimal
from django.core.exceptions import ValidationError
# Create your models here.

class GastosVehiculos(models.Model):
    
    proyecto = models.ForeignKey(Proyectos, related_name= 'gastos_vehiculos',on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculos, related_name='vehiculos',on_delete=models.CASCADE)
    cantidad_combustible = models.FloatField()
    monto = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    iva = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    proveedor = models.CharField(max_length=100,null=False)
    ubicacion = models.CharField(max_length=100,null=False)
    conductor = models.CharField(max_length=100,null=False)
    fecha = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.proyecto.proyecto} - {self.vehiculo}"
    
class GastosGenerales(models.Model):
    proyecto = models.ForeignKey(Proyectos, related_name= 'gastos_generales',on_delete=models.CASCADE)
    concepto = models.CharField(max_length=255,null=False)
    comprador = models.CharField(max_length=255,null=False)
    monto = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    iva = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    notas = models.TextField(blank=True)
    proveedor = models.CharField(max_length=100,null=False)
    fecha = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.proyecto.proyecto} - {self.concepto}"
    
class GastosMateriales(models.Model):
    proyecto = models.ForeignKey(Proyectos, related_name= 'gastos_materiales',on_delete=models.CASCADE)
    concepto = models.CharField(max_length=255,null=False)
    comprador = models.CharField(max_length=255,null=False)
    monto = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    iva = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    descripcion = models.TextField(blank=True)
    proveedor = models.CharField(max_length=100,null=False)
    fecha = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.proyecto.proyecto} - {self.concepto}"
    
class GastosSeguridad(models.Model):
    proyecto = models.ForeignKey(Proyectos, related_name= 'gastos_seguridad',on_delete=models.CASCADE)
    concepto = models.CharField(max_length=255,null=False)
    comprador = models.CharField(max_length=255,null=False)
    monto = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    iva = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    descripcion = models.TextField(blank=True)
    proveedor = models.CharField(max_length=100,null=False)
    fecha = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.proyecto.proyecto} - {self.concepto}"
    
class GastosManoObra(models.Model):
    proyecto = models.ForeignKey(Proyectos, related_name= 'gastos_mano_obra',on_delete=models.CASCADE)
    nomina = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    imss = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    infonavit = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    isn = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    isr = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    horas_extras = models.DecimalField(max_digits=10, decimal_places=2,null=False, default=Decimal('0.00'))
    monto = models.DecimalField(max_digits=10, decimal_places=2,default=Decimal('0.00'))
    lote = models.IntegerField(unique=True)
    fecha = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.proyecto.proyecto}"
    
class GastosEquipos(models.Model):

    TIEMPO_RENTA = [
        ('RENTA_MENSUAL','renta mensual'),
        ('RENTA_SEMANAL','renta semanal'),
        ('RENTA_DIARIA','renta diaria'),
        ('PROPIEDAD','Propiedad')
    ]

    proyecto = models.ForeignKey(Proyectos, related_name= 'gastos_equipos',on_delete=models.CASCADE)
    concepto = models.CharField(max_length=255,null=False)
    comprador = models.CharField(max_length=255,null=False)
    tiempo_renta = models.CharField(max_length=100,choices=TIEMPO_RENTA,default='RENTA_MENSUAL')
    monto = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    iva = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    descripcion = models.TextField(blank=True)
    proveedor = models.CharField(max_length=100,null=False)
    fecha = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.proyecto.proyecto} - {self.concepto}"
    
class Ingresos(models.Model):

    proyecto = models.ForeignKey(Proyectos,related_name='ingresos',on_delete=models.CASCADE)
    concepto = models.CharField(max_length=255,null=False)
    monto = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    iva = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    referencia = models.CharField(max_length=100,null=False)
    fecha = models.DateField(default=timezone.now,null=False)

    def __str__(self):
        return self.proyecto.proyecto