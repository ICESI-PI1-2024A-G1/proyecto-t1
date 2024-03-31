$(document).ready(function () {
    /**
     * Initializes DataTable with the given table ID.
     *
     * @param {string} tableId - The ID of the table to initialize DataTable on.
     */
    DataTableInit("teamsTable")

    // Fetch CSRF token from meta tag
    const csrfTokenMeta = document.querySelector('meta[name="csrf_token"]');
    const csrftoken = csrfTokenMeta.getAttribute('content');

    /**
     * Handles click event on delete team button.
     */
    $(".delete-team").click(function() {
        var teamId = $(this).data("team-id");

        /**
         * Confirms and deletes the team if confirmed.
         */
        if (confirm("¿Estás seguro de que quieres eliminar este equipo?")) {
            $.ajax({
                url: `/teams/delete/${teamId}/`,
                type: "DELETE",
                beforeSend: function(xhr) {
                    // Set CSRF token in request header
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                success: function(response) {
                    // Reload the page after successful deletion
                    location.reload();
                },
                error: function(xhr, status, error) {
                    console.error(error);
                    // Display an alert for error in deletion
                    alert("Error deleting team");
                }
            });
        }
    });
});
