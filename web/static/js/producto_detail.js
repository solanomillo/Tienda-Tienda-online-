// static/js/producto_detail.js
document.addEventListener('DOMContentLoaded', function() {
    const increment = document.getElementById('increment');
    const decrement = document.getElementById('decrement');
    const quantityInput = document.querySelector('input[name="cantidad"]');

    if (increment && decrement && quantityInput) {
        increment.addEventListener('click', function() {
            let value = parseInt(quantityInput.value);
            quantityInput.value = value + 1;
        });

        decrement.addEventListener('click', function() {
            let value = parseInt(quantityInput.value);
            if (value > 1) {
                quantityInput.value = value - 1;
            }
        });
    }
});