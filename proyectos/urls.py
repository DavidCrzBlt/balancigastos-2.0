from django.urls import path
from proyectos import views

from proyectos.views import export_proyectos_to_excel, export_project_details_to_excel, actualizar_progreso


app_name = 'proyectos'

urlpatterns = [
    
    path("registrar-proyecto/",views.CrearProyectoView.as_view(),name="registrar_proyecto"),
    path("editar-proyecto/<slug:slug>",views.EditarProyectoView.as_view(),name="editar_proyecto"),
    path('eliminar_proyecto/<slug:slug>/', views.EliminarProyectoView.as_view(), name='eliminar_proyecto'),
    path("",views.ProyectosListView.as_view(),name="proyectos"),
    path("proyectos/<slug:slug>/",views.ProyectosDetailView.as_view(),name="detalles_proyecto"),
    path('proyectos/<slug:slug>/toggle-estatus/', views.toggle_estatus_proyecto, name='toggle_estatus_proyecto'),
    path('exportar-proyectos/', export_proyectos_to_excel, name='export_proyectos_to_excel'),
    path('exportar-detalles-proyecto/<slug:proyecto_slug>/', export_project_details_to_excel, name='export_project_details_to_excel'),
    path("actualizar-progreso/<slug:slug>/",actualizar_progreso,name="actualizar_progreso"),

]