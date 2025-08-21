from django.urls import path
from empleados import views

app_name = 'empleados'

urlpatterns = [
    # Empleados
    path('lista-empleados/', views.EmpleadosListView.as_view(), name='empleados'),
    path('crear-empleado/', views.CrearEmpleadoView.as_view(), name='crear_empleado'),
    path('editar-empleado/<int:pk>/', views.EditarEmpleadoView.as_view(), name='editar_empleado'),
    path('eliminar-empleado/<int:pk>/', views.EliminarEmpleadoView.as_view(), name='eliminar_empleado'),

    # Asistencias
    path('<slug:slug>/asistencias/', views.AsistenciasListView.as_view(), name='asistencias'),
    path('<slug:slug>/asistencias/crear/', views.CrearAsistenciaView.as_view(), name='crear_asistencia'),
    path('asistencias/editar/<int:pk>/', views.EditarAsistenciaView.as_view(), name='editar_asistencia'),
    path('asistencias/eliminar/<int:pk>/', views.EliminarAsistenciaView.as_view(), name='eliminar_asistencia'),
]
