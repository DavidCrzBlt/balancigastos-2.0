from django import forms
from django.utils.timezone import now
from django.core.exceptions import ValidationError

from .models import Empleados, Asistencias

# Aquí van los forms

class EmpleadosForm(forms.ModelForm):
    class Meta:
        model = Empleados
        fields = ['nombres','apellido_paterno','apellido_materno','rfc','infonavit','imss']

    def clean(self):
        cleaned_data = super().clean()
        rfc = cleaned_data.get('rfc')  
        if Empleados.objects.filter(rfc=rfc).exists():
            raise forms.ValidationError("Ya existe un empleado con ese RFC.")
        return cleaned_data
    
class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencias
        exclude = ['proyecto']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')

        # Check if the date is in the future
        if fecha > now().date():
            raise ValidationError('No puedes registrar una asistencia con una fecha futura.')

        return fecha

class AsistenciaExcelForm(forms.Form):
    archivo_excel = forms.FileField()

class NominasExcelForm(forms.Form):
    archivo_excel = forms.FileField()