# Generated by Django 5.1 on 2024-09-22 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipos_y_vehiculos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculos',
            name='valor_original',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
