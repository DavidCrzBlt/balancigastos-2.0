from django.urls import path
from . import views
from .views import pagina_principal

app_name = 'clientes'

urlpatterns = [
    path('registro-clientes',views.crear_cliente, name='crear_cliente'),
    path('',pagina_principal,name='pagina_principal')
]
