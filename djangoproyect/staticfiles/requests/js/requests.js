const changeStatus = id => {
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();
    var newStatus = $('#newStatusSelect').val();
    $.ajax({
        url: '/requests/change-status/' + id,
        method: 'POST',
        data: {
            newStatus: newStatus,
            csrfmiddlewaretoken: csrftoken
        },
        success: function (response) {
            $('#status_' + id).text(newStatus);
        },
        error: function () {
            alert('Error al cambiar el estado de la solicitud.');
        }
    });
    $('#detailsModal').modal('hide');
}

$(document).ready(function () {
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