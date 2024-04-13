// selecciona todos los campos de entrada excepto el total
var inputs = document.querySelectorAll('input[type=number]:not(#total)');

// agrega un evento de cambio a cada campo de entrada
inputs.forEach(function(input) {
    input.addEventListener('change', updateTotal);
});

// actualiza el total
function updateTotal() {
    var total = 0;

    // suma los valores de todos los campos de entrada
    inputs.forEach(function(input) {
        total += Number(input.value);
    });

    // actualiza el campo de entrada total
    document.getElementById('total').value = total;
}