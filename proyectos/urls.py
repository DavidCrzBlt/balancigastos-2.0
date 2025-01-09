from django.urls import path
from . import views
from proyectos.views import ProyectosListView, ProyectosDetailView, export_proyectos_to_excel, export_project_details_to_excel, actualizar_progreso


app_name = 'proyectos'

urlpatterns = [
    
    path("registrar-proyecto/",views.registrar_proyecto,name="registrar_proyecto"),
    path('eliminar_proyecto/<slug:slug>/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path("",ProyectosListView.as_view(),name="proyectos"),
    path("proyectos/<slug:slug>/",ProyectosDetailView.as_view(),name="detalles_proyecto"),
    path('proyectos/<slug:slug>/toggle-estatus/', views.toggle_estatus_proyecto, name='toggle_estatus_proyecto'),
    path('exportar-proyectos/', export_proyectos_to_excel, name='export_proyectos_to_excel'),
    path('exportar-detalles-proyecto/<slug:proyecto_slug>/', export_project_details_to_excel, name='export_project_details_to_excel'),
    path("actualizar-progreso/<slug:slug>/",actualizar_progreso,name="actualizar_progreso"),

]