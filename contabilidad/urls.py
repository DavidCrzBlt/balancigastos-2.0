from django.urls import path
from . import views
from contabilidad.views import IngresosListView, ListaGastosView, ListaCategoriasGastoView,ListaNominasView
from contabilidad.views import CrearIngresoView,CrearGastoView, CrearCategoriaGastoView, CrearNominaView

app_name = 'contabilidad'

urlpatterns = [
    # Path de listas
    path("<slug:slug>/ingresos",IngresosListView.as_view(),name="ingresos"),
    path("<slug:slug>/gastos",ListaGastosView.as_view(),name="gastos"),
    path("categorias/",ListaCategoriasGastoView.as_view(),name="categorias_gasto"),
    path("<slug:slug>/nominas",ListaNominasView.as_view(),name="nominas"),
    
    # Path de registros
    path("registrar-ingreso/<slug:slug>",CrearIngresoView.as_view(),name="registro_ingresos"),
    path("registrar-gasto/<slug:slug>",CrearGastoView.as_view(),name="registro_gastos"),
    path("registrar-nomina/<slug:slug>",CrearNominaView.as_view(),name="registro_nomina"),
    path("registrar-categoria-gasto/",CrearCategoriaGastoView.as_view(),name="registro_categoria_gastos"),

    # Path de ediciones
 
    # Path de eliminaciones
    


    
]