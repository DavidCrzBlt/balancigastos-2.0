from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('registro-clientes',views.crear_cliente, name='crear_cliente'),
    path('lista-clientes/',views.lista_clientes, name='lista_clientes'),
]
