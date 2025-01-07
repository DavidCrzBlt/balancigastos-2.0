from django.urls import path
from . import views

app_name = 'presupuestos'

urlpatterns = [
    path("datos-presupuesto/",views.ingresar_datos_generales_presupuesto,name="ingresar_datos_cabecera_presupuesto"),
    path("",views.lista_presupuestos,name="presupuestos"),
]