from django.db import models
from django.utils.text import slugify
from decimal import Decimal
# Create your models here.

class Proyectos(models.Model):

    proyecto = models.CharField(max_length=255)
    clave_proyecto = models.CharField(max_length=100,unique=True)
    empresa = models.CharField(max_length=255)
    estatus = models.BooleanField(default=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    iva = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.proyecto)
        super(Proyectos, self).save(*args, **kwargs)

    def __str__(self):
        return self.proyecto