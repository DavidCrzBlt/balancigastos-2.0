from django import forms
from .models import Proyectos
from django.core.exceptions import ValidationError

class ProyectosForm(forms.ModelForm):
    class Meta:
        model = Proyectos
        fields = ['proyecto','clave_proyecto','empresa']

        # widgets = {
        #     'proyecto':forms.TextInput(attrs={
        #         'class': '',
        #         'placeholder':'Nombre del proyecto'
        #     }),
        #     'empresa':forms.TextInput(attrs={
        #         'class': '',
        #         'placeholder':'Nombre de la empresa'
        #     }),
        #     'estatus': forms.Select(attrs={
        #         'class': ''
        #     }),
        #     'total':forms.NumberInput(attrs={
        #         'class': '',
        #         'placeholder': 'Total'
        #     }),
        # }

