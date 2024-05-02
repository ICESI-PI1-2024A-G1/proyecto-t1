// adds a new row to the table
document.addEventListener('DOMContentLoaded', (event) => {
    var rowCount = localStorage.getItem('rowCount');
    if (rowCount !== null) {
        obj = rowCount - 2;
        for (var i = 0; i < obj; i++) {
            addRow();
        }
    }

    document.getElementById('addRow').addEventListener('click', addRow);

    // removes the last row from the table
    document.getElementById('removeRow').addEventListener('click', function() {
        var table = document.querySelector('tbody');
        var rows = Array.from(table.children);
        var totalsRowIndex = rows.findIndex(row => row.id === 'totals');

        // Check if there is a row above the totals row
        if (totalsRowIndex > 0) {
            var rowToRemove = rows[totalsRowIndex - 1];
            table.removeChild(rowToRemove);
        }

        updateTotals();
        updateRowCount();
    });
});

// detects changes in the input fields
document.querySelector('tbody').addEventListener('input', function(event) {
    if (event.target.tagName.toLowerCase() === 'input') {
        updateTotals();
    }
});

// adds a new row to the table
function addRow() {
    var table = document.querySelector('tbody');
    var newRow = document.createElement('tr');

    var rowNumber = table.getElementsByTagName('tr').length - 4;

    for (var i = 0; i < 4; i++) {
        var newCell = document.createElement('td');
        var input = document.createElement('input');
        input.type = i < 4 ? 'text' : 'number';
        input.className = 'form-control';
        if (i == 2) {
            input.placeholder = '0';
        }
        input.name = ['category', 'provider', 'pesos', 'concept'][i] + '_' + rowNumber;
        input.value = form_data[input.name] || '';
        newCell.appendChild(input);
        newRow.appendChild(newCell);
    }

    var totalsRow = document.getElementById('totals');
    table.insertBefore(newRow, totalsRow);

    updateTotals();
    updateRowCount();
};

// updates the totals row
function updateTotals() {
    var total = 0;

    // get all the rows except the totals, advance, employeeBalance, and icesiBalance rows
    var rows = Array.from(document.querySelector('tbody').children);
    rows = rows.filter(row => !['totals', 'advance', 'employeeBalance', 'icesiBalance'].includes(row.id));

    // sum all the input fields for each row
    rows.forEach(function(row) {
        var input = row.children[2].firstChild;
        total += Number(input.value);
    });

    // update the total field in the totals row
    document.getElementById('total').value = total;

    // calculate "Saldo a favor del empleado" and "Saldo a favor de ICESI"
    var totalAdvance = Number(document.getElementById('advanceTotal').value);
    var employeeBalance = total > totalAdvance ? total - totalAdvance : 0;
    var icesiBalance = totalAdvance > total ? totalAdvance - total : 0;

    // update "Saldo a favor del empleado" and "Saldo a favor de ICESI" fields
    document.getElementById('employeeBalanceValue').value = employeeBalance;
    document.getElementById('icesiBalanceValue').value = icesiBalance;
}

function updateRowCount() {
    var rowCount = document.getElementById('tableAdvanceLegalization').rows.length - 5;
    localStorage.setItem('rowCount', rowCount);
}