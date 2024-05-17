/**
 * Changes the status of a request.
 *
 * @param {number} id - The ID of the request to change status for.
 */
const changeStatus = id => {
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();
    var newStatus = $('#newStatusSelect').val();
    var reason = $('#reasonTextarea').val();
    if (reason === '') {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Debe ingresar un motivo para cambiar el estado de la solicitud.'
        });
        return;
    }
    Swal.fire({
        title: '¿Estás seguro?',
        text: '¿Quieres establecer la solicitud en "' + newStatus + '"? Esta acción no se puede deshacer.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, cambiar',
        cancelButtonText: 'No, cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.showLoading();
            $.ajax({
                url: '/requests/change-status/' + id + "/",
                method: 'POST',
                data: {
                    newStatus: newStatus,
                    reason: reason,
                    csrfmiddlewaretoken: csrftoken
                },
                success: function (response) {
                    window.location.href = "/requests/?changeStatusDone";
                },
                error: function (xhr, status, error) {
                    window.location.href = "/requests/?changeStatusFailed";
                }
            });
            $('#detailsModal').modal('hide');
        }
    });
}

$(document).ready(function () {   
    /**
     * Initializes DataTable with the given table ID and handles search functionality.
     *
     * @param {string} tableId - The ID of the table to initialize DataTable on.
     */
    DataTableInit("requestsTable", 10, [
        {
            "targets": 1, // This is only applied to the date column
            "orderable": true,
            "type": "date" // Using ordering by date
        },
        {
            "targets": 2, // This is only applied to the date column
            "orderable": true,
            "type": "date" // Using ordering by date
        },
    ])
    $("#performSearchButton").on('click', function () {
        var query = $("#searchBar").val() || '';
        $.ajax({
            url: "/requests/search/" + query,
            data: { 'q': query },
            success: function (data) {
                var tbody = $('#requestsTable tbody');
                tbody.empty();
                data.forEach(function (item) {
                    var fila = `
                            <tr>
                                <td>${item.document || ''}</td>
                                <td>${item.applicant || ''}</td>
                                <td>${item.manager || ''}</td>
                                <td>${item.initial_date || ''}</td>
                                <td>${item.final_date || ''}</td>
                                <td>${item.past_days || ''}</td>
                                <td>
                                <button class="btn btn-link edit-btn" data-request-id="${item.id}">
                                <i class="fa fa-edit text-secondary"></i>
                                </button>
                                <span id="status_${item.id}">${item.status || ''}</span>
                                </td>
                            </tr>
                        `;
                    tbody.append(fila);
                });
            },
            error: function (xhr, status, error) {
                console.log("Error en la solicitud AJAX:", error);
            }
        });
    });
});