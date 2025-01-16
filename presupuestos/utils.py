import os
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML


def generar_pdf(template_path, context, output_filename):
    """
    Genera un PDF a partir de una plantilla HTML y un contexto.

    :param template_path: Ruta de la plantilla HTML (dentro de Django).
    :param context: Diccionario con el contexto para renderizar la plantilla.
    :param output_filename: Nombre del archivo PDF a generar.
    :return: Ruta completa del archivo PDF generado.
    """
    # Renderizar la plantilla con el contexto
    html_string = render_to_string(template_path, context)

    # Crear la ruta del archivo PDF en la carpeta personalizada
    carpeta_pdf = os.path.join(settings.BASE_DIR, 'archivos_pdf')
    output_path = os.path.join(carpeta_pdf, output_filename)
    
    # Crear la carpeta "archivos_pdf" si no existe
    os.makedirs(carpeta_pdf, exist_ok=True)
    
    # Convertir HTML a PDF
    HTML(string=html_string).write_pdf(output_path)
    
    return output_path
