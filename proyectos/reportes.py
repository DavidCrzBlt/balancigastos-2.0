import openai
import json
from django.conf import settings
from .models import Proyectos
from contabilidad.views import recalcular_totales_proyecto

from decimal import Decimal
from openai import OpenAI

# Inicia funciones

client = OpenAI(api_key = settings.OPENAI_API_KEY)

model="gpt-4o-mini"

# Función para convertir Decimals a float en el diccionario
def decimal_a_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def generar_reporte(project_id):
    project = Proyectos.objects.get(id=project_id)

    # Consulta tus datos de gastos desde el modelo
    totales = recalcular_totales_proyecto(project_id)
    # Convierte el diccionario `totales` a una cadena JSON formateada
    totales_json = json.dumps(totales, indent=4, ensure_ascii=False, default=decimal_a_float)
    
    # Construye el prompt para generar el reporte
    prompt = f"Genera un reporte detallado para el proyecto {project.proyecto}:\n\n"
    prompt += totales_json
    prompt += "Por favor proporciona un resumen sobre estos datos financieros."

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Procesa la respuesta de OpenAI
    reporte = completion.choices[0].message.content
    return reporte
