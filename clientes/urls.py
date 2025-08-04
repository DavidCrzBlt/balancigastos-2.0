from django.urls import path
from . import views
from .views import pagina_principal,CrearClienteView

app_name = 'clientes'

urlpatterns = [
    path("registrar-cliente",CrearClienteView.as_view(), name = "crear_cliente"),
    path("",pagina_principal, name="pagina_principal"),
]
