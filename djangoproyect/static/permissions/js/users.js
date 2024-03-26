$(document).ready(function () {
    $("#performSearchButton").on('click', function () {
        var query = $("#searchBar").val() || 'None';
        $.ajax({
            url: "/permissions/search/" + query,
            data: { 'q': query },
            success: function (data) {
                var tbody = $('#usersTable tbody');
                tbody.empty();
                data.forEach(function (item) {
                    var fila = `
                            <tr>
                                <td>${item.id || ''}${item.is_superuser ? ' (SU) ' : ''}</td>
                                <td>${item.first_name || ''}</td>
                                <td>${item.last_name || ''}</td>
                                <td>${item.email || ''}</td>
                                <td><input type="checkbox" ${item.is_superuser ? 'disabled' : ''} ${item.is_staff ? 'checked' : ''}></td>
                                <td><input type="checkbox" ${item.is_superuser ? 'disabled' : ''} ${item.is_leader ? 'checked' : ''}></td>
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