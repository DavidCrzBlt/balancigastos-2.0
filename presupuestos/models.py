from django.db import models
from decimal import Decimal
from django.utils import timezone
from django.db.models import Max
from django.utils.text import slugify

# Create your models here.


class DatosPresupuesto(models.Model):

    num_presupuesto = models.CharField(max_length=50,unique=True,null=False)
    nombre_proyecto = models.CharField(max_length=80,null=False)
    cliente = models.CharField(max_length=40)
    responsable = models.CharField(max_length=40)
    contacto = models.CharField(max_length=50)
    version = models.PositiveIntegerField(default=1,null=False)
    fecha = models.DateField(default=timezone.now)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre_proyecto)
        if not self.num_presupuesto:  # Solo generar si no existe
            año_actual = timezone.now().year % 100
            iniciales_empresa = "CCO"
            ultimo_numero = (
                DatosPresupuesto.objects.filter(num_presupuesto__startswith=f"{iniciales_empresa}{año_actual}")
                .aggregate(max_num=Max("num_presupuesto"))["max_num"]
            )

            if ultimo_numero:
                # Extraer el número secuencial y sumarle 1
                secuencia = int(ultimo_numero[-5:]) + 1
            else:
                secuencia = 1  # Primer número del año

            self.num_presupuesto = f"{iniciales_empresa}{año_actual}{str(secuencia).zfill(5)}"

        super(DatosPresupuesto,self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_proyecto


class PrecioUnitarioPresupuesto(models.Model):

    UNIDADES = [
        ('servicio', 'Servicio'),
        ('m2', 'Metros cuadrados'),
        ('ml','Metros lineales'),
        ('pza','Pieza')
    ]

    presupuesto = models.ForeignKey(DatosPresupuesto, related_name= 'precio_unitario',on_delete=models.CASCADE)
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
    