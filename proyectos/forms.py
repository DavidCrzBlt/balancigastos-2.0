from django import forms
from .models import Proyectos
from django.core.exceptions import ValidationError

class ProyectosForm(forms.ModelForm):
    class Meta:
        model = Proyectos
        fields = ['proyecto','clave_proyecto','empresa','fecha_fin_estimada','presupuesto_estimado','ganancia_estimada']

        widgets = {
            'fecha_fin_estimada': forms.DateInput(attrs={'type': 'date'}),
        }

