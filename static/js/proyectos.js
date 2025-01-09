document.addEventListener('DOMContentLoaded', function () {
    // Seleccionamos todos los íconos de basura en las filas de proyectos
    const eliminarBtns = document.querySelectorAll('.eliminar-btn');

    eliminarBtns.forEach(function (btn) {
        // Asociamos el evento de clic a cada ícono de basura
        btn.addEventListener('click', function () {
            const proyectoNombre = btn.getAttribute('data-nombre');
            const proyectoSlug = btn.getAttribute('data-slug');
            eliminar_proyecto(proyectoSlug, proyectoNombre);
        });
    });
});

function eliminar_proyecto(slug, nombre_proyecto) {
    // Mostramos un cuadro de confirmación para eliminar el proyecto
    let confirmacion = prompt(`¿Estás seguro de querer eliminar el proyecto ${nombre_proyecto}? Para confirmar, escribe el nombre del proyecto.`);

    if (confirmacion === nombre_proyecto) {
        // Usamos la plantilla de la URL y reemplazamos el slug dinámicamente
        let eliminarUrl = eliminarUrlTemplate.replace('slug_placeholder', slug);

        // Redirigimos a la URL de eliminación en Django
        window.location.href = eliminarUrl;
    } else {
        alert('El nombre del proyecto no coincide. Eliminación cancelada.');
    }
}
