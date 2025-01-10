function formatearMoneda(valor) {
    return new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(valor);
}

function calcular_totales() {
    let subtotalGeneral = 0;

    // Recorrer todas las filas con la clase 'subtotal'
    document.querySelectorAll("tr").forEach((row) => {
        // Buscar el 'td' con la clase 'subtotal' dentro de cada fila
        const subtotalTd = row.querySelector("td.subtotal");
        
        if (subtotalTd) {
            // Obtener el valor de subtotal y sumarlo
            const subtotal = parseFloat(subtotalTd.innerHTML) || 0; // Convertir a número o usar 0
            subtotalGeneral += subtotal;
        }
    });

    // Calcular IVA y total general
    const iva = subtotalGeneral * 0.16; // IVA al 16%
    const totalGeneral = subtotalGeneral + iva;

    // Mostrar los resultados en los elementos correspondientes
    document.getElementById("subtotal-general").innerHTML = `<strong>${formatearMoneda(subtotalGeneral)}</strong>`;
    document.getElementById("iva").innerHTML = `<strong>${formatearMoneda(iva)}</strong>`;
    document.getElementById("total-general").innerHTML = `<strong>${formatearMoneda(totalGeneral)}</strong>`;
}

// Calcular el subtotal general, IVA y total
calcular_totales();