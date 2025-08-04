from django import forms
from .models import Empleados

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

class AsistenciaExcelForm(forms.Form):
    archivo_excel = forms.FileField()

class NominasExcelForm(forms.Form):
    archivo_excel = forms.FileField()