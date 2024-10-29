from django import forms
from .models import Vehiculos

class VehiculosForm(forms.ModelForm):
    class Meta:
        model = Vehiculos
        fields = ['vehiculo','marca','color','placas','combustible','valor_original']