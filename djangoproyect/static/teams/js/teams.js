$(document).ready(function () {
    $(document).on('click', '#userList li', function () {
        $(this).toggleClass('active');
        var hasSelectedUser = $('#userList li.active').length > 0;
        $('#addMemberSubmit').prop('disabled', !hasSelectedUser);
    });
    $('#addMemberModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var teamId = button.data('team-id');
        var modal = $(this);

        $.get(`/teams/add-member/${teamId}`, function (data) {
            $("#userList").empty();
            data.forEach(function (user) {
                $("#userList").append(`<li data-user-id="${user.id}" style="cursor:pointer" class="list-group-item">${user.first_name} ${user.last_name} (@${user.username})</li>`);
            });
        });

        modal.find('#addMemberSubmit').attr('data-team-id', teamId);
        var tableId = `#team_${teamId}_table`;
        modal.data('table-id', tableId);
    });

    $('#addMemberSubmit').on('click', function () {
        var teamId = $(this).data('team-id');
        var selectedUsers = [];

        $('#userList li.active').each(function () {
            selectedUsers.push($(this).data('user-id'));
        });

        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

        $.post(`/teams/add-member/${teamId}`, { users: selectedUsers, csrfmiddlewaretoken: csrftoken }, function (response) {
            var tableId = $('#addMemberModal').data('table-id');
            var tableBody = $(`${tableId} tbody`);

            response.users.forEach(function (user) {
                tableBody.append(
                    '<tr>' +
                    `<td> ${user.first_name} ${user.last_name} </td>` +
                    '<td>Miembro</td>' +
                    '<td><button class="btn text-danger delete-member" data-team-id="' + teamId + '" data-member-id="' + user.id + '">Eliminar</button></td>' +
                    '</tr>'
                );
            });

            $('#userList li.active').removeClass('active');
            $('#addMemberModal').modal('hide');
        });
    });
    $(".delete-member").click(function () {
        if (!confirm("¿Estás seguro de que quieres eliminar a este miembro?")) return false;
        var teamId = $(this).data("team-id");
        var memberId = $(this).data("member-id");
        $.ajax({
            url: "/teams/delete-member/" + teamId + "/" + memberId,
            type: "GET",
            success: function (response) {
                $("#member_row_" + memberId).remove();
            },
            error: function () {
                alert("Error al eliminar al miembro");
            }
        });
    });
});