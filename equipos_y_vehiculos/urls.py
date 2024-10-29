from django.urls import path
from . import views

app_name = 'equipos_y_vehiculos'

urlpatterns = [
    path('equipos/',views.index,name='index'),
    path("registrar-vehiculo",views.registro_vehiculos, name="registro_vehiculos"),
]