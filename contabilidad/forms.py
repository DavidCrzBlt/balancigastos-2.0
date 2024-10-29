from django import forms
from .models import GastosVehiculos, GastosGenerales, GastosEquipos, GastosSeguridad, GastosManoObra, GastosMateriales, Ingresos
from django.utils import timezone
from django.core.exceptions import ValidationError

 # Obtén la hora actual en la zona horaria local
now = timezone.now().date()

class GastosVehiculosForm(forms.ModelForm):
    class Meta:
        model = GastosVehiculos
        fields = ['vehiculo','cantidad_combustible','monto','ubicacion', 'proveedor','conductor','fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),  # Calendar widget for 'fecha'
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')

        # Check if the date is in the future
        if fecha > now:
            raise ValidationError('No puedes registrar un gasto con una fecha futura.')

        return fecha 

class GastosGeneralesForm(forms.ModelForm):
    class Meta:
        model = GastosGenerales
        fields = ['concepto','comprador','monto','notas','proveedor','fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),  # Calendar widget for 'fecha'
        }
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')

        # Check if the date is in the future
        if fecha > now:
            raise ValidationError('No puedes registrar un gasto con una fecha futura.')

        return fecha
    
class GastosMaterialesForm(forms.ModelForm):
    class Meta:
        model = GastosMateriales
        fields = ['concepto','comprador','monto','descripcion','proveedor','fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),  # Calendar widget for 'fecha'
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')

        # Check if the date is in the future
        if fecha > now:
            raise ValidationError('No puedes registrar un gasto con una fecha futura.')

        return fecha 
    
class GastosManoObraForm(forms.ModelForm):
    class Meta:
        model = GastosManoObra
        fields = ['nomina','imss','infonavit','isn','isr','fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),  # Calendar widget for 'fecha'
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')

        # Check if the date is in the future
        if fecha > now:
            raise ValidationError('No puedes registrar un gasto con una fecha futura.')

        return fecha 
    
class GastosEquiposForm(forms.ModelForm):
    class Meta:
        model = GastosEquipos
        fields = ['concepto','comprador','tiempo_renta','monto','descripcion', 'proveedor','fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),  # Calendar widget for 'fecha'
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')

        # Check if the date is in the future
        if fecha > now:
            raise ValidationError('No puedes registrar un gasto con una fecha futura.')

        return fecha

class GastosSeguridadForm(forms.ModelForm):
    class Meta:
        model = GastosSeguridad
        fields = ['concepto','comprador','monto','descripcion', 'proveedor','fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),  # Calendar widget for 'fecha'
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')

        # Check if the date is in the future
        if fecha > now:
            raise ValidationError('No puedes registrar un gasto con una fecha futura.')

        return fecha 
    
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
        if fecha > now:
            raise ValidationError('No puedes registrar un gasto con una fecha futura.')

        return fecha