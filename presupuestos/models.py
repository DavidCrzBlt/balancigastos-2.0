from django.db import models
from decimal import Decimal
from django.utils import timezone

# Create your models here.


class DatosPresupuesto(models.Model):

    num_presupuesto = models.CharField(max_length=50,unique=True,null=False)
    nombre_proyecto = models.CharField(max_length=80,null=False)
    cliente = models.CharField(max_length=40)
    responsable = models.CharField(max_length=40)
    contacto = models.CharField(max_length=50)
    version = models.PositiveIntegerField(default=1,null=False)
    fecha = models.DateField(default=timezone.now)


class PrecioUnitarioPresupuesto(models.Model):

    UNIDADES = [
        ('servicio', 'Servicio'),
        ('m2', 'Metros cuadrados'),
        ('ml','Metros lineales'),
        ('pza','Pieza')
    ]

    id_presupuesto = models.ForeignKey(DatosPresupuesto, related_name= 'precio_unitario',on_delete=models.CASCADE)
    concepto = models.concepto = models.TextField(null=False)
    unidad = models.CharField(max_length=30,choices=UNIDADES)
    materiales = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=Decimal('0.00'))
    mano_obra = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=Decimal('0.00'))
    examenes_med_dc3 = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=Decimal('0.00'))
    equipos = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=Decimal('0.00'))
    epp = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=Decimal('0.00'))
    costo_directo = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=Decimal('0.00'))
    costo_indirecto = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=Decimal('0.00'))
    costo_financiamiento = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=Decimal('0.00'))
    utilidad = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=Decimal('0.00'))
    precio_unitario = models.DecimalField(max_digits=10,decimal_places=2,null=False,default=Decimal('0.00'))

class HistorialPresupuesto(models.Model):
    id_presupuesto = models.ForeignKey(DatosPresupuesto,related_name="historial_presupuesto",on_delete=models.CASCADE)
    version = models.PositiveIntegerField(default=1, null=False)
    presupuesto = models.JSONField()
    fecha = models.DateField(default=timezone.now)
    