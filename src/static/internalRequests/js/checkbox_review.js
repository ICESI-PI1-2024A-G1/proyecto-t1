// Mark all checkboxes during review
$(document).ready(function() {
    var allChecked = false;
    $('#markAll').click(function() {
        allChecked = !allChecked;
        $('input:checkbox').prop('checked', allChecked);
        if (allChecked) {
            document.getElementById('markAll').innerHTML = 'Desmarcar todos';
        } else {
            document.getElementById('markAll').innerHTML = 'Marcar todos';
        }
    });
});