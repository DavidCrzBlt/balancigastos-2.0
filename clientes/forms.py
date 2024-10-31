from django import forms
from clientes.models import Cliente, DominioCliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'dominio']

    def clean_dominio(self):
        dominio = self.cleaned_data['dominio']
        # Asegúrate de que el dominio sea único
        if Cliente.objects.filter(dominio=dominio).exists():
            raise forms.ValidationError("Este dominio ya está en uso.")
        return dominio
