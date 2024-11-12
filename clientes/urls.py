from django.urls import path
from . import views


app_name = 'clientes'

urlpatterns = [
    path("",views.crear_cliente, name = "crear_cliente"),
    # path("",pagina_principal, name="pagina_principal"),
]
