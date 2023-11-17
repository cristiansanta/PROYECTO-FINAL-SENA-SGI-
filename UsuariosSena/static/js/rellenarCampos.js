$(document).ready(function () {
    // Cuando se cambia el nombre del elemento
    $('input[name="nombreElemento"]').on('input', function () {
        var selectedElement = $(this).val();
        if (selectedElement) {
            $.ajax({
                url: '/get-serial-by-element-name',
                type: 'GET',
                data: { 'elementName': selectedElement },
                success: function (response) {
                    if (response.serialNumber) {
                        $('input[name="serialSenaElemento"]').val(response.serialNumber);
                    }
                    if (response.valorUnidad) {
                        $('input[name="valorUnidadElemento"]').val(response.valorUnidad);
                    }
                    if (response.Stock) {
                        $('input[name="disponibles"]').val(response.Stock);  // Actualizar el campo Disponibles
                    }
                },
                error: function (xhr, status, error) {
                    console.error("Error: ", error);
                }
            });
        } else {
            // Limpiar los campos si el nombre del elemento está vacío
            $('input[name="serialSenaElemento"]').val('');
            $('input[name="valorUnidadElemento"]').val('');
            $('input[name="disponibles"]').val('');
            $('input[name="cantidadElemento"]').val('');
            $('input[name="valorTotalElemento"]').val('');
            $('input[name="observacionesPrestamo"]').val('');
        }
    });

    // Cuando se cambia el número de serie
    $('input[name="serialSenaElemento"]').on('input', function () {
        var serialNumber = $(this).val();
        if (serialNumber) {
            $.ajax({
                url: '/get-element-name-by-serial',
                type: 'GET',
                data: { 'serialNumber': serialNumber },
                success: function (response) {// Actualizar el campos
                    if (response.elementName) {
                        $('input[name="nombreElemento"]').val(response.elementName);
                    }
                    if (response.valorUnidad) {
                        $('input[name="valorUnidadElemento"]').val(response.valorUnidad);
                    }
                    if (response.Stock) {
                        $('input[name="disponibles"]').val(response.Stock);
                    }
                },
                error: function (xhr, status, error) {
                    console.error("Error: ", error);
                }
            });
        } else {
            // Limpiar los campos si el número de serie está vacío
            $('input[name="nombreElemento"]').val('');
            $('input[name="valorUnidadElemento"]').val('');
            $('input[name="disponibles"]').val('');
            $('input[name="cantidadElemento"]').val('');
            $('input[name="valorTotalElemento"]').val('');
            $('input[name="observacionesPrestamo"]').val('');
        }
    });
});