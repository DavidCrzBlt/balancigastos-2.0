from django import forms
from .models import Empleados

class EmpleadosForm(forms.ModelForm):
    class Meta:
        model = Empleados
        fields = ['nombres','apellido_paterno','apellido_materno','rfc','infonavit','imss']

class AsistenciaExcelForm(forms.Form):
    archivo_excel = forms.FileField()

class NominasExcelForm(forms.Form):
    archivo_excel = forms.FileField()