from django import forms
from .models import DatosPresupuesto
from django.utils import timezone
from django.core.exceptions import ValidationError

 # Obtén la hora actual en la zona horaria local
now = timezone.now().date()

class DatosPresupuestoForm(forms.ModelForm):
    class Meta:
        model = DatosPresupuesto
        fields = ['nombre_proyecto','cliente','responsable','contacto', 'version']