from django import forms
from .models import Proyectos
from django.core.exceptions import ValidationError
from django.utils.text import slugify


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

    def clean(self):
        cleaned_data = super().clean()
        proyecto = cleaned_data.get('proyecto')
        if proyecto:
            slug = slugify(proyecto)
            if Proyectos.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Ya existe un proyecto con este nombre (slug duplicado).")
        return cleaned_data

