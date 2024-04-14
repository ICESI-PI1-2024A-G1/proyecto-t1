// selects all input fields except the total field
var inputs = document.querySelectorAll('input[type=number]:not(#total)');

// adds an event listener to each input field
inputs.forEach(function(input) {
    input.addEventListener('change', updateTotal);
});

// updates the total field
function updateTotal() {
    var total = 0;

    // sum all the input fields
    inputs.forEach(function(input) {
        total += Number(input.value);
    });

    // update the total field
    document.getElementById('total').value = total;
}