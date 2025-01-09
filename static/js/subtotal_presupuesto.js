function formatearMoneda(valor) {
    return new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(valor);
}

function calcular_presupuesto(row) {
    const cantidadInput = row.querySelector("td:nth-child(4) input");
    const precioUnitarioValue = row.querySelector("td:nth-child(5)");
    const subtotalInput = row.querySelector("td:nth-child(6) input");

    // Procesar solo si las celdas con inputs existen
    if (cantidadInput && subtotalInput) {
        const cantidad = parseFloat(cantidadInput.value) || 0; // Convertir a número o usar 0 si está vacío
        const precioUnitario = parseFloat(precioUnitarioValue.textContent) || 0; // Convertir a número o usar 0 si está vacío

        const subtotal = cantidad * precioUnitario; // Calcular subtotal
        subtotalInput.value = subtotal.toFixed(2); // Mostrar el subtotal con 2 decimales
    }
}

function calcular_totales() {
    let subtotalGeneral = 0;

    // Iterar sobre todas las filas válidas (solo las que tienen inputs en la columna de subtotal)
    document.querySelectorAll("tbody tr").forEach((row) => {
        const subtotalInput = row.querySelector("td:nth-child(6) input");
        if (subtotalInput) {
            const subtotal = parseFloat(subtotalInput.value) || 0; // Convertir a número o usar 0
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

// Función principal que actualiza todo
function actualizar_presupuesto() {
    // Calcular los subtotales por fila
    document.querySelectorAll("tbody tr").forEach((row) => calcular_presupuesto(row));
    
    // Calcular el subtotal general, IVA y total
    calcular_totales();
}

// Agregar listeners a los inputs de cantidad
document.addEventListener("DOMContentLoaded", () => {
    const cantidadInputs = document.querySelectorAll("tbody td:nth-child(4) input");
    cantidadInputs.forEach((cantidadInput) => {
        cantidadInput.addEventListener("input", () => actualizar_presupuesto());
    });

    // Ejecutar una vez al cargar la página para que los totales iniciales sean correctos
    actualizar_presupuesto();
});