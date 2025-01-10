function calcular_costo_directo() {
    var materiales = document.getElementById('materiales').value||0;
    var mano_obra = document.getElementById('mano_obra').value||0;
    var examenes_med_dc3 = document.getElementById('examenes_med_dc3').value||0;
    var equipos = document.getElementById('equipos').value||0;
    var epp = document.getElementById('epp').value||0;
    var costo_directo = document.getElementById('costo_directo');

    var suma = parseFloat(materiales) + parseFloat(mano_obra) + parseFloat(examenes_med_dc3) + parseFloat(equipos) + parseFloat(epp);

    costo_directo.value = suma.toFixed(2);
    
}

function calcular_precio_unitario(){
    var meses_financiamiento = document.getElementById('meses_financiamiento').value||0;
    var costo_directo = document.getElementById('costo_directo').value||0;
    var porcentaje_indirecto = document.getElementById('costo_indirecto').value||0;
    var porcentaje_financiamiento = document.getElementById('costo_financiamiento').value||0;
    var porcentaje_sobrecosto = document.getElementById('sobrecosto').value||0;

    var costo_indirecto = parseFloat(costo_directo) * parseFloat(porcentaje_indirecto)/100;
    var costo_financiamiento = (parseFloat(costo_indirecto)+parseFloat(costo_directo)) * parseFloat(porcentaje_financiamiento) * parseFloat(meses_financiamiento)/100;
    var sobrecosto = (parseFloat(costo_directo) + parseFloat(costo_indirecto) + parseFloat(costo_financiamiento)) * parseFloat(porcentaje_sobrecosto)/100; 
    var precio_unitario_suma = parseFloat(costo_directo) + parseFloat(costo_indirecto) + parseFloat(costo_financiamiento) + parseFloat(sobrecosto);

    var precio_unitario = document.getElementById('precio_unitario');
    precio_unitario.value = precio_unitario_suma.toFixed(2);
}

function calcular_subtotal() {
    var precio_unitario = document.getElementById('precio_unitario').value||0;
    var cantidad = document.getElementById('cantidad').value||0;

    var calculo_subtotal = parseFloat(cantidad) * parseFloat(precio_unitario);

    var subtotal = document.getElementById('subtotal');
    subtotal.value = calculo_subtotal.toFixed(2);    
}

function ejecutar_calculos(){
    calcular_costo_directo();
    calcular_precio_unitario();
    calcular_subtotal();
}

// Escucha eventos en los campos que afectan el cálculo
document.getElementById('materiales').addEventListener('input', ejecutar_calculos);
document.getElementById('mano_obra').addEventListener('input', ejecutar_calculos);
document.getElementById('examenes_med_dc3').addEventListener('input', ejecutar_calculos);
document.getElementById('equipos').addEventListener('input', ejecutar_calculos);
document.getElementById('epp').addEventListener('input', ejecutar_calculos);
document.getElementById('costo_indirecto').addEventListener('input', ejecutar_calculos);
document.getElementById('costo_financiamiento').addEventListener('input', ejecutar_calculos);
document.getElementById('meses_financiamiento').addEventListener('input', ejecutar_calculos);
document.getElementById('sobrecosto').addEventListener('input', ejecutar_calculos);
document.getElementById('cantidad').addEventListener('input', ejecutar_calculos);
