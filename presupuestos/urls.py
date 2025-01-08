from django.urls import path
from . import views

app_name = 'presupuestos'

urlpatterns = [
    path("presupuesto/",views.ingresar_datos_generales_presupuesto,name="ingresar_datos_cabecera_presupuesto"),
    path("presupuesto/<slug:slug>/precios-unitarios/",views.ingresar_precios_unitarios,name="ingresar_precios_unitarios"),
    path("presupuesto/<slug:slug>/ajuste-presupuesto/",views.ajuste_presupuesto,name="ajuste_presupuesto"),
    path("",views.lista_presupuestos,name="presupuestos"),
]