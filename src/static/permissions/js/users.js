/**
 * Initializes DataTable with the given table ID.
 *
 * @param {string} tableId - The ID of the table to initialize DataTable on.
 */
$(document).ready(function () {
    DataTableInit("usersTable")
     /**
     * Handles click event on the search button.
     *
     * @param {Event} event - The click event object.
     */
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
                            <tr id="user_${item.id}">
                                <td>${item.id || ''}${item.is_superuser ? ' (SU) ' : ''}</td>
                                <td>${item.last_name || ''}</td>
                                <td>${item.first_name || ''}</td>
                                <td>${item.email || ''}</td>
                                <td><input type="radio" name="permission_${item.id}" value="is_leader" ${item.is_superuser ? 'disabled' : ''} ${item.is_leader ? 'checked' : ''}></td>
                                <td><input type="radio" name="permission_${item.id}" value="is_member" ${item.is_superuser ? 'disabled' : ''} ${item.is_member ? 'checked' : ''}></td>
                                <td><input type="radio" name="permission_${item.id}" value="is_applicant" ${item.is_superuser ? 'disabled' : ''} ${item.is_applicant ? 'checked' : ''}></td>
                                <td><input type="radio" name="permission_${item.id}" value="is_applicant" ${item.is_superuser ? 'disabled' : ''} ${item.is_none ? 'checked' : ''}></td>
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

    /**
     * Handles click event on the save button.
     *
     * @param {Event} event - The click event object.
     */
    $(document).on('click', '#saveButton', function() {
        var radios = $('#usersTable tbody input[type="radio"]:checked');
        var newValues = [];

        radios.each(function() {
            var radio = $(this);
            var id = radio.closest('tr').attr('id').split('_')[1];
            var permission = radio.val();

            var newValue = { id: id, permission: permission };
            newValues.push(newValue);
        });

        $.ajax({
            url: '/permissions/update_user_permissions/',
            type: 'POST',
            data: JSON.stringify(newValues),
            contentType: 'application/json; charset=utf-8',
            success: function(response) {
                if (response.message) {
                    var alertClass = response.status === 'success' ? 'alert-success' : 'alert-danger';
                    var alertHtml = '<div class="alert ' + alertClass + ' alert-dismissible fade show" role="alert">' +
                        response.message +
                        '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                        '</div>';
                    $('#messageContainer').html(alertHtml);
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});