import os
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML, CSS


def generar_pdf(template_path, context, output_filename,request,usuario):
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
    
    # Use STATICFILES_DIRS for CSS during development
    css_path = settings.STATICFILES_DIRS[0] + '/css/presupuestos.css'
       
    # Crear la carpeta "archivos_pdf" si no existe
    os.makedirs(carpeta_pdf, exist_ok=True)

    imagen_url = usuario.profile_picture.url

    print(f'Dentro de generar_pdf {request.build_absolute_uri(imagen_url)}')
    
    # Convert HTML to PDF
    HTML(string=html_string, base_url=request.build_absolute_uri(imagen_url)).write_pdf(
        output_path,
        stylesheets=[CSS(css_path)],
        presentational_hints=True
    )

    return output_path
