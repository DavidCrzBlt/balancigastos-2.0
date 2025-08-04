from django import forms
from clientes.models import Cliente, DominioCliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre']
