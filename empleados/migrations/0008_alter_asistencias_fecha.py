# Generated by Django 5.1 on 2024-09-22 22:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0007_alter_asistencias_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencias',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2024, 9, 22, 22, 17, 29, 243916)),
        ),
    ]
