from django.urls import path
from contabilidad import views


app_name = 'contabilidad'

urlpatterns = [
    # Path de listas
    path("<slug:slug>/ingresos",views.IngresosListView.as_view(),name="ingresos"),
    path("<slug:slug>/gastos",views.ListaGastosView.as_view(),name="gastos"),
    path("categorias/",views.ListaCategoriasGastoView.as_view(),name="categorias_gasto"),
    path("<slug:slug>/nominas",views.ListaNominasView.as_view(),name="nominas"),
    
    # Path de registros
    path("registrar-ingreso/<slug:slug>",views.CrearIngresoView.as_view(),name="registro_ingresos"),
    path("registrar-gasto/<slug:slug>",views.CrearGastoView.as_view(),name="registro_gastos"),
    path("registrar-nomina/<slug:slug>",views.CrearNominaView.as_view(),name="registro_nomina"),
    path("registrar-categoria-gasto/",views.CrearCategoriaGastoView.as_view(),name="registro_categoria_gastos"),

        # Path de ediciones
    path("editar-ingreso/<slug:slug>/<int:pk>", views.ActualizarIngresoView.as_view(), name="editar_ingreso"),
    path("editar-gasto/<slug:slug>/<int:pk>", views.ActualizarGastoView.as_view(), name="editar_gasto"),
    path("editar-nomina/<slug:slug>/<int:pk>", views.ActualizarNominaView.as_view(), name="editar_nomina"),
    path("editar-categoria-gasto/<int:pk>", views.ActualizarCategoriaGastoView.as_view(), name="editar_categoria_gasto"),

    # Path de eliminaciones
    path("eliminar-ingreso/<slug:slug>/<int:pk>", views.EliminarIngresoView.as_view(), name="eliminar_ingreso"),
    path("eliminar-gasto/<slug:slug>/<int:pk>", views.EliminarGastoView.as_view(), name="eliminar_gasto"),
    path("eliminar-nomina/<slug:slug>/<int:pk>", views.EliminarNominaView.as_view(), name="eliminar_nomina"),
    path("eliminar-categoria-gasto/<int:pk>", views.EliminarCategoriaGastoView.as_view(), name="eliminar_categoria_gasto"),

    
]