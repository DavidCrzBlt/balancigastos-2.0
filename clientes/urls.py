from django.urls import path
from . import views
from .views import pagina_principal,CrearClienteView
from clientes import views

app_name = 'clientes'

urlpatterns = [
    path("registrar-cliente",CrearClienteView.as_view(), name = "crear_cliente"),
    path("lista-clientes",views.ClienteListView.as_view(), name = "lista_clientes"),
    path("",pagina_principal, name="pagina_principal"),
]
