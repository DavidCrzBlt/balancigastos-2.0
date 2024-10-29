from django.db import models

# Create your models here.

class Vehiculos(models.Model):

    TIPO_COMBUSTIBLE = [
        ('GASOLINE','Gasolina'),
        ('DIESEL','Diesel'),
        ('ELECTRIC','Eléctrico')
    ]

    vehiculo = models.CharField(max_length=255,null=False)
    marca = models.CharField(max_length=80,null=False)
    color = models.CharField(max_length=80,null=False)
    placas = models.CharField(max_length=60,null=False)
    combustible = models.CharField(max_length=30,choices=TIPO_COMBUSTIBLE,default='GASOLINE')
    valor_original = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.vehiculo