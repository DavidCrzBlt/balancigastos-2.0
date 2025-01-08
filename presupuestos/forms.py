from django import forms
from .models import DatosPresupuesto, PrecioUnitarioPresupuesto
from django.utils import timezone
from django.core.exceptions import ValidationError

 # Obtén la hora actual en la zona horaria local
now = timezone.now().date()

class DatosPresupuestoForm(forms.ModelForm):
    class Meta:
        model = DatosPresupuesto
        fields = ['nombre_proyecto','cliente','responsable','contacto', 'version']

class PreciosUnitariosForm(forms.ModelForm):
    class Meta:
        model = PrecioUnitarioPresupuesto
        fields = ['concepto','unidad','materiales','mano_obra','examenes_med_dc3','equipos','epp','costo_directo','costo_indirecto','costo_financiamiento','meses_financiamiento','utilidad','precio_unitario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['materiales'].widget.attrs.update({
            'id': 'materiales'
        })

        self.fields['mano_obra'].widget.attrs.update({
            'id': 'mano_obra'
        })

        self.fields['examenes_med_dc3'].widget.attrs.update({
            'id': 'examenes_med_dc3'
        })

        self.fields['equipos'].widget.attrs.update({
            'id': 'equipos'
        })

        self.fields['epp'].widget.attrs.update({
            'id': 'epp'
        })

        ##-----------------------------------##
        self.fields['precio_unitario'].widget.attrs.update({
            'readonly': 'readonly',  # Desactiva el campo
            'class': 'disabled-field',  # Clase para aplicar estilos CSS específicos
            'id': 'precio_unitario'
        })

        self.fields['costo_directo'].widget.attrs.update({
            'readonly': 'readonly',  # Desactiva el campo
            'class': 'disabled-field',  # Clase para aplicar estilos CSS específicos
            'id': 'costo_directo'
        })
        ##-----------------------------------##
        self.fields['costo_indirecto'].widget.attrs.update({
            'id': 'costo_indirecto',
            'placeholder': 'Ejemplo: 10',  # Texto guía en el campo
            'class': 'percent-field',       # Clase para estilizar si es necesario
            'title': 'Introduce el porcentaje de costo indirecto',
        })

        self.fields['costo_financiamiento'].widget.attrs.update({
            'id': 'costo_financiamiento',
            'placeholder': 'Ejemplo: 10',  # Texto guía en el campo
            'class': 'percent-field',       # Clase para estilizar si es necesario
            'title': 'Introduce el porcentaje de costo de financiamiento',
        })

        self.fields['meses_financiamiento'].widget.attrs.update({
            'id': 'meses_financiamiento',
            'placeholder': 'Ejemplo: 10',  
            'title': 'Introduce el número de meses a financiar',
        })

        self.fields['utilidad'].widget.attrs.update({
            'id': 'sobrecosto',
            'placeholder': 'Ejemplo: 15',
            'class': 'percent-field',
            'title': 'Introduce el porcentaje de utilidad',
        })
    
