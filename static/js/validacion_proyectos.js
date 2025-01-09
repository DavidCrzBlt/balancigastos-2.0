document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const gananciaInput = document.querySelector('input[name="ganancia_estimada"]');
    const presupuestoInput = document.querySelector('input[name="presupuesto_estimado"]');
    const claveInput = document.querySelector('input[name="clave_proyecto"]');
    const submitButton = form.querySelector('button[type="submit"]');

    // Función de validación
    function validarFormulario(event) {
        // Validación de ganancia estimada y presupuesto estimado
        const ganancia = parseFloat(gananciaInput.value);
        const presupuesto = parseFloat(presupuestoInput.value);

        if (ganancia > presupuesto) {
            alert('La ganancia estimada no puede ser mayor que el presupuesto estimado.');
            event.preventDefault(); // Evita el envío del formulario
            return false;
        }

        // Validación de clave de proyecto (al menos una letra)
        const clave = claveInput.value;
        const regex = /[A-Za-z]/; // Expresión regular que valida al menos una letra
        if (!regex.test(clave)) {
            alert('La clave de proyecto debe contener al menos una letra.');
            event.preventDefault(); // Evita el envío del formulario
            return false;
        }

        return true;
    }

    // Event listener para el submit del formulario
    form.addEventListener('submit', function(event) {
        validarFormulario(event);
    });
});
