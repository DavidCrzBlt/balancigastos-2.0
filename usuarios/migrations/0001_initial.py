from django.db import migrations, models
import django.contrib.auth.models
import django.utils.timezone

class Migration(migrations.Migration):

    initial = True  # Indica que esta es la primera migración para este modelo

    dependencies = [
        
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(
                    max_length=150, 
                    unique=True,
                    error_messages={'unique': "A user with that username already exists."}
                )),
                ('first_name', models.CharField(max_length=150, blank=True)),
                ('last_name', models.CharField(max_length=150, blank=True)),
                ('email', models.EmailField(
                    max_length=254, 
                    unique=True,
                    error_messages={'unique': "A user with that email already exists."}
                )),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('tenant', models.ForeignKey(to='clientes.Client', on_delete=models.CASCADE)),
                ('groups', models.ManyToManyField(
                    to='auth.Group', 
                    related_name='customuser_set', 
                    blank=True
                )),
                ('user_permissions', models.ManyToManyField(
                    to='auth.Permission', 
                    related_name='customuser_set', 
                    blank=True
                )),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('profile_picture', models.ImageField(upload_to='profile_pictures/', blank=True, null=True)),
                ('user', models.OneToOneField(to='usuarios.CustomUser', on_delete=models.CASCADE)),
            ],
        ),
    ]
