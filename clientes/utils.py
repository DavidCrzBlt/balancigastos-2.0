from django.http import HttpRequest
import os

###--------------------------------------------------------------------------------###

def get_subdomain(request: HttpRequest):
    # Obtener el hostname completo (subdominio.dominio.com)
    subdomain = request.get_host()
    return subdomain


    