
$(document).ready(function () {
    const csrfTokenMeta = document.querySelector('meta[name="csrf_token"]');
    const csrftoken = csrfTokenMeta.getAttribute('content');
    $(".delete-team").click(function() {
        var teamId = $(this).data("team-id");
        if (confirm("¿Estás seguro de que quieres eliminar este equipo?")) {
            $.ajax({
                url: `/teams/delete/${teamId}/`,
                type: "DELETE",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                success: function(response) {
                    location.reload()
                },
                error: function(xhr, status, error) {
                    console.error(error);
                    alert("Error al eliminar el equipo");
                }
            });
        }
    });
});