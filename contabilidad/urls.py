from django.urls import path
from . import views
from contabilidad.views import GastosVehiculosListView, GastosGeneralesListView, GastosMaterialesListView, GastosManoObraListView, GastosEquiposListView, IngresosListView, GastosSeguridadListView

app_name = 'contabilidad'

urlpatterns = [
    # Path de listas
    path("<slug:slug>/gastos-generales",GastosGeneralesListView.as_view(),name="gastos_generales"),
    path("<slug:slug>/gastos-vehiculos",GastosVehiculosListView.as_view(),name="gastos_vehiculos"),
    path("<slug:slug>/gastos-materiales",GastosMaterialesListView.as_view(),name="gastos_materiales"),
    path("<slug:slug>/gastos-equipos",GastosEquiposListView.as_view(),name="gastos_equipos"),
    path("<slug:slug>/gastos-seguridad",GastosSeguridadListView.as_view(),name="gastos_seguridad"),
    path("<slug:slug>/gastos-mano-obra",GastosManoObraListView.as_view(),name="gastos_mano_obra"),
    path("<slug:slug>/ingresos",IngresosListView.as_view(),name="ingresos"),
    
    # Path de registros
    path("registrar-gastos-generales/<slug:slug>",views.registro_gastos_generales, name="registro_gastos_generales"),
    path("registrar-gastos-vehiculos/<slug:slug>",views.registro_gastos_vehiculos, name="registro_gastos_vehiculos"),
    path("registrar-gastos-materiales/<slug:slug>",views.registro_gastos_materiales,name="registro_gastos_materiales"),
    path("registrar-gastos-equipos/<slug:slug>",views.registro_gastos_equipos,name="registro_gastos_equipos"),
    path("registrar-gastos-seguridad/<slug:slug>",views.registro_gastos_seguridad,name="registro_gastos_seguridad"),
    path("registrar-gastos-mano-obra/<slug:slug>",views.registro_gastos_mano_obra,name="registro_gastos_mano_obra"),
    path("registrar-ingreso/<slug:slug>",views.registro_ingresos,name="registro_ingresos"),

    # Path de ediciones
    path("editar-gastos-generales/<slug:slug>/<int:gasto_id>",views.registro_gastos_generales, name="editar_gastos_generales"),
    path("editar-gastos-vehiculos/<slug:slug>/<int:gasto_id>",views.registro_gastos_vehiculos, name="editar_gastos_vehiculos"),
    path("editar-gastos-materiales/<slug:slug>/<int:gasto_id>",views.registro_gastos_materiales,name="editar_gastos_materiales"),
    path("editar-gastos-equipos/<slug:slug>/<int:gasto_id>",views.registro_gastos_equipos,name="editar_gastos_equipos"),
    path("editar-gastos-seguridad/<slug:slug>/<int:gasto_id>",views.registro_gastos_seguridad,name="editar_gastos_seguridad"),
    path("editar-ingreso/<slug:slug>/<int:ingreso_id>",views.registro_ingresos,name="editar_ingresos"),

    # Path de eliminaciones
    path("eliminar-gastos-mano-obra/<slug:slug>/<int:gasto_id>",views.eliminar_gastos_mano_obra,name="eliminar_gastos_mano_obra"),
    path("eliminar-gastos-generales/<slug:slug>/<int:gasto_id>",views.eliminar_gastos_generales,name="eliminar_gastos_generales"),
    path("eliminar-gastos-vehiculos/<slug:slug>/<int:gasto_id>",views.eliminar_gastos_vehiculos,name="eliminar_gastos_vehiculos"),
    path("eliminar-gastos-materiales/<slug:slug>/<int:gasto_id>",views.eliminar_gastos_materiales,name="eliminar_gastos_materiales"),
    path("eliminar-gastos-equipos/<slug:slug>/<int:gasto_id>",views.eliminar_gastos_equipos,name="eliminar_gastos_equipos"),
    path("eliminar-gastos-seguridad/<slug:slug>/<int:gasto_id>",views.eliminar_gastos_seguridad,name="eliminar_gastos_seguridad"),
    path("eliminar-ingresos/<slug:slug>/<int:gasto_id>",views.eliminar_ingresos,name="eliminar_ingresos"),

    
]