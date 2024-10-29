# Generated by Django 5.1 on 2024-09-22 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proyectos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proyecto', models.CharField(max_length=255)),
                ('empresa', models.CharField(max_length=255)),
                ('estatus', models.BooleanField(default=True)),
                ('total', models.FloatField(default=0)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]
