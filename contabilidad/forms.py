from django import forms
from django.utils.timezone import now
from django.core.exceptions import ValidationError

from .models import Ingresos, Gasto, CategoriaGasto, NominaEmpleado


class IngresosForm(forms.ModelForm):
    class Meta:
        model = Ingresos
        fields = ['concepto','monto','referencia','fecha']

        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),  # Calendar widget for 'fecha'
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')

        # Check if the date is in the future
        if fecha > now().date():
            raise ValidationError('No puedes registrar un ingreso con una fecha futura.')

        return fecha
    
class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['categoria','concepto','proveedor','comprador','monto','descripcion','fecha']

        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),  # Calendar widget for 'fecha'
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')

        # Check if the date is in the future
        if fecha > now().date():
            raise ValidationError('No puedes registrar un gasto con una fecha futura.')

        return fecha
    
class CategoriaGastoForm(forms.ModelForm):
    class Meta:
        model = CategoriaGasto
        fields = ['nombre']

class NominaEmpleadoForm(forms.ModelForm):
    class Meta:
        model = NominaEmpleado
        exclude = ['lote', 'proyecto']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'})
        }
