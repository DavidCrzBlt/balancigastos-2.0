# Generated by Django 5.1 on 2024-11-11 16:20

import django.db.models.deletion
import django.utils.timezone
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proyectos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empleados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=255)),
                ('apellido_paterno', models.CharField(max_length=255)),
                ('apellido_materno', models.CharField(max_length=255)),
                ('rfc', models.CharField(max_length=100, unique=True)),
                ('infonavit', models.BooleanField(default=False)),
                ('imss', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Asistencias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asistencias', models.BooleanField(default=True)),
                ('horas_extras', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=4)),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asistencias', to='proyectos.proyectos')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asistencias', to='empleados.empleados')),
            ],
        ),
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lotes', to='proyectos.proyectos')),
            ],
        ),
        migrations.CreateModel(
            name='Salario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salario', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('infonavit', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('imss', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('isr', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('horas_extras', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('lote', models.IntegerField(editable=False)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salario', to='empleados.empleados')),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salario', to='proyectos.proyectos')),
            ],
        ),
    ]
