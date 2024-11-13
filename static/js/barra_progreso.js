function actualizarBarraProgreso(nuevoValor) {
    var barraProgreso = document.getElementById('progress-bar');
    var contenedorProgreso = document.getElementById('progress-bar-container');

    // Actualizamos el valor y el texto
    barraProgreso.style.width = nuevoValor + '%';
    barraProgreso.innerText = nuevoValor + '%';

    // Actualizamos el aria-valuenow para accesibilidad
    contenedorProgreso.setAttribute('aria-valuenow', nuevoValor);
}

