document.addEventListener("DOMContentLoaded", function () {
    // Obtener los elementos del formulario por su nombre
    var cantidadInput = document.getElementsByName('cantidadElemento')[0];
    var valorUnidadInput = document.getElementsByName('valorUnidadElemento')[0];
    var valorTotalInput = document.getElementsByName('valorTotalElemento')[0];

    // Función para calcular el valor total
    function calcularValorTotal() {
        var cantidad = parseInt(cantidadInput.value) || 0;
        var valorUnidad = parseInt(valorUnidadInput.value) || 0;
        var valorTotal = cantidad * valorUnidad;
        valorTotalInput.value = valorTotal; // Asegurar dos decimales
    }

    // Evento para detectar cambios y calcular el total
    cantidadInput.addEventListener('change', calcularValorTotal);
    valorUnidadInput.addEventListener('change', calcularValorTotal);

    // Calcular inicialmente en caso de que los campos ya tengan valores
    calcularValorTotal();
});