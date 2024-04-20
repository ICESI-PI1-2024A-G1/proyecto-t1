window.onload = function() {
    var inputs = document.querySelectorAll('.budget-input');
    var totalInput = document.getElementById('total');

    inputs.forEach(function(input) {
        input.addEventListener('input', function() {
            var sum = 0;
            inputs.forEach(function(input) {
                if (input.value) {
                    var value = parseFloat(input.value);
                    if (!isNaN(value)) {
                        sum += value;
                    }
                }
            });
            totalInput.value = sum;
        });
    });
};