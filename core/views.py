from django.views.generic.edit import FormView
from django.urls import reverse_lazy

class FormularioGenericoView(FormView):
    template_name = 'form_template.html'
    success_url = reverse_lazy('inicio')  # se puede sobreescribir desde la subclase

    # Propiedades que se usan para personalizar el template sin reescribir get_context_data
    page_title = 'Formulario'
    form_title = 'Formulario'
    button_text = 'Enviar'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        context['form_title'] = self.form_title
        context['button_text'] = self.button_text
        return context

    def form_valid(self, form):
        """
        Guarda automáticamente si el form es de modelo.
        Puedes sobreescribir esto en la subclase si necesitas lógica adicional.
        """
        self.object = form.save()
        return super().form_valid(form)
