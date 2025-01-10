document.addEventListener('DOMContentLoaded', function() {
    const botonConfirmar = document.getElementById('confirmar-presupuesto');
    
    botonConfirmar.addEventListener('click', function() {
        const idsPreciosUnitarios = [];
        
        // Recorrer las filas de la tabla para obtener los IDs de los precios unitarios
        document.querySelectorAll('tbody tr .subtotal').forEach(function(fila) {
            const idConcepto = fila.getAttribute('data-id');  // Obtener el ID del concepto de la fila
            idsPreciosUnitarios.push(idConcepto);  // Agregar el ID a la lista
        });

        // Obtener el slug del proyecto
        var slug = document.getElementById('confirmar-presupuesto').getAttribute('data-slug');
        console.log(idsPreciosUnitarios);
        console.log(slug);
        // Enviar los datos a Django
        enviarPresupuesto(idsPreciosUnitarios, slug);
    });

    // Función para enviar los datos a Django
    function enviarPresupuesto(idsPreciosUnitarios, slug) {
        // Construir la URL con el slug dinámicamente
        let confirmarPresupuestoUrl = confirmarPresupuestoUrlTemplate.replace('slug_placeholder', slug);
        console.log(confirmarPresupuestoUrl);
        fetch(confirmarPresupuestoUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()  // Obtener el token CSRF para proteger la solicitud
            },
            body: JSON.stringify({
                precios_unitarios_ids: idsPreciosUnitarios
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Presupuesto confirmado exitosamente');
                // Realizar alguna acción adicional si es necesario, como redirigir
                // Redirigir solo después de recibir la respuesta exitosa
                window.location.href = data.redirect_url;  // Si el backend devuelve un URL de redirección
            } else {
                alert('Hubo un error al confirmar el presupuesto');
            }
        })
        .catch(error => {
            console.error('Error al enviar los datos:', error);
            alert('Error en la comunicación con el servidor');
        });
    }

    // Función para obtener el token CSRF
    function getCsrfToken() {
        const cookieValue = document.cookie.match(/csrftoken=([^;]+)/);
        return cookieValue ? cookieValue[1] : '';
    }
});
