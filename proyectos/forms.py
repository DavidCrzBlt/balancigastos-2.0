from django import forms
from .models import Proyectos
from django.core.exceptions import ValidationError

class ProyectosForm(forms.ModelForm):
    class Meta:
        model = Proyectos
        fields = ['proyecto','clave_proyecto','empresa','fecha_fin_estimada','presupuesto_estimado','ganancia_estimada']

        widgets = {
            'fecha_fin_estimada': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'proyecto': forms.TextInput(attrs={'required': True}),
            'clave_proyecto': forms.TextInput(attrs={'required': True, 'pattern': '[A-Za-z0-9]+', 'title': 'Debe contener al menos una letra y solo letras o números.'}),
            'empresa': forms.TextInput(attrs={'required': True}),
            'presupuesto_estimado': forms.NumberInput(attrs={'required': True}),
            'ganancia_estimada': forms.NumberInput(attrs={'required': True}),
        }
