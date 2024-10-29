from django.urls import path
from . import views
from .views import EmpleadosListView, AsistenciasListView, NominasListView
app_name = 'empleados'

urlpatterns = [
    path("empleados/",EmpleadosListView.as_view(),name="empleados"),
    path("registro-empleado/",views.registro_empleados,name="registro_empleados"),
    path("asistencias/<slug:slug>",AsistenciasListView.as_view(),name="asistencias"),
    path("registro_asistencias/<slug:slug>",views.registro_asistencias,name="registro_asistencias"),
    path("registro_nominas/<slug:slug>",views.registro_nominas,name="registro_nominas"),
    path("nominas/<slug:slug>/<int:lote>",NominasListView.as_view(),name="nominas"),
    path("eliminar-empleado/<int:empleado_id>",views.eliminar_empleado,name="eliminar_empleado"),
    path("editar-empleado/<int:empleado_id>",views.editar_empleado,name="editar_empleado"),
    path("eliminar-asistencia/<slug:slug>/<int:asistencia_id>",views.eliminar_asistencia,name="eliminar_asistencia"),
]