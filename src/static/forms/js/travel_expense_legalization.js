// adds a new row to the table
document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('addRow').addEventListener('click', function() {
        event.preventDefault();
        var table = document.querySelector('tbody');
        var newRow = document.createElement('tr');

        // Get the current number of rows
        var currentRowCount = table.querySelectorAll('tr:not(#totals):not(#advance):not(#employeeBalance):not(#icesiBalance)').length;

        for (var i = 0; i < 7; i++) {
            var newCell = document.createElement('td');
            var input = document.createElement('input');
            input.type = i < 4 ? 'text' : 'number';
            input.className = 'form-control';
            if (i >= 4) {
                input.placeholder = '0';
                input.id = ['total', 'advance', 'employeeBalance', 'icesiBalance'][i - 4] + (currentRowCount + 1);
                input.name = input.id;
            }
            newCell.appendChild(input);
            newRow.appendChild(newCell);
        }

        var totalsRow = document.getElementById('totals');
        table.insertBefore(newRow, totalsRow);

        updateTotals();
    });
    // removes the last row from the table
    document.getElementById('removeRow').addEventListener('click', function() {
        event.preventDefault();
        var table = document.querySelector('tbody');
        var rows = Array.from(table.children);
        var totalsRowIndex = rows.findIndex(row => row.id === 'totals');

        // Check if there is a row above the totals row
        if (totalsRowIndex > 0) {
            var rowToRemove = rows[totalsRowIndex - 1];
            table.removeChild(rowToRemove);
        }

        updateTotals();
    });
});

// detects changes in the input fields
document.querySelector('tbody').addEventListener('input', function(event) {
    if (event.target.tagName.toLowerCase() === 'input') {
        updateTotals();
    }
});

// updates the totals row
function updateTotals() {
    var totals = [0, 0, 0];

    // get all the rows except the totals, advance, employeeBalance, and icesiBalance rows
    var rows = Array.from(document.querySelector('tbody').children);
    rows = rows.filter(row => !['totals', 'advance', 'employeeBalance', 'icesiBalance'].includes(row.id));

    // sum all the input fields for each row
    rows.forEach(function(row) {
        var inputs = Array.from(row.children).slice(4).map(td => td.firstChild);

        inputs.forEach(function(input, index) {
            totals[index] += Number(input.value);
        });
    });

    // update the total fields in the totals row
    totals.forEach(function(total, index) {
        document.getElementById('total' + (index + 1)).value = total;
    });

    // calculate "Saldo a favor del empleado" and "Saldo a favor de ICESI"
    var totalAdvance = [1, 2, 3].map(i => Number(document.getElementById('advanceTotal' + i).value));
    var employeeBalance = totals.map((total, i) => total > totalAdvance[i] ? total - totalAdvance[i] : 0);
    var icesiBalance = totals.map((total, i) => totalAdvance[i] > total ? total - totalAdvance[i] : 0);

    // update "Saldo a favor del empleado" and "Saldo a favor de ICESI" fields
    employeeBalance.forEach((balance, i) => {
        document.getElementById('employeeBalance' + (i + 1)).value = balance;
    });

    icesiBalance.forEach((balance, i) => {
        document.getElementById('icesiBalance' + (i + 1)).value = balance;
    });
}