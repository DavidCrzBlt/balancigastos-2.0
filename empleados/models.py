from django.db import models
from proyectos.models import Proyectos
from django.utils import timezone
from decimal import Decimal

# Create your models here.

class Empleados(models.Model):
    nombres = models.CharField(max_length=255,null=False)
    apellido_paterno = models.CharField(max_length=255,null=False)
    apellido_materno = models.CharField(max_length=255,null=False)
    rfc = models.CharField(max_length=100,null=False,unique=True)
    infonavit = models.BooleanField(default=False)
    imss = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.rfc

class Asistencias(models.Model):
    empleado = models.ForeignKey(Empleados,related_name="asistencias",on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyectos,related_name="asistencias",on_delete=models.CASCADE)
    asistencias = models.BooleanField(default=True,null=False)
    horas_extras = models.DecimalField(max_digits=4, decimal_places=2,null=False,default=Decimal('0.00'))
    fecha = models.DateField(default=timezone.now,null=False)

    def __str__(self):
        return self.empleado

class Salario(models.Model):
    empleado = models.ForeignKey(Empleados,related_name="salario",on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyectos,related_name="salario",on_delete=models.CASCADE)
    salario = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    infonavit = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    imss = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    isr = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    horas_extras = models.DecimalField(max_digits=10, decimal_places=2,null=False,default=Decimal('0.00'))
    lote = models.IntegerField(editable=False)

class Lote(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    proyecto = models.ForeignKey(Proyectos,related_name='lotes',on_delete=models.CASCADE)

    @classmethod
    def obtener_nuevo_lote(cls,proyecto):
        try:
            project = Proyectos.objects.get(proyecto=proyecto, estatus=True)
            print(f"Proyecto encontrado: {proyecto.proyecto}")  # Depuración
        except Proyectos.DoesNotExist:
            print("El proyecto no existe o no está activo.")  # Depuración
            raise ValueError("El proyecto no existe o no está activo.")
            
        nuevo_lote = cls.objects.create(proyecto=project)
        return nuevo_lote  # El ID del objeto será nuestro número de lote.
    