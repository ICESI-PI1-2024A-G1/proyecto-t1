/**
 * Initializes the DataTable for the specified table element.
 * @param {string} tableId - The ID of the table element to initialize as a DataTable.
 */
$(document).ready(function () {
    DataTableInit("teamsTable");

    // Fetch CSRF token from meta tag
    const csrfTokenMeta = document.querySelector('meta[name="csrf_token"]');
    const csrftoken = csrfTokenMeta.getAttribute('content');

    /**
     * Event handler for clicking on the delete team button.
     */
    $(".delete-team").click(function() {
        var teamId = $(this).data("team-id");
        if (confirm("Are you sure you want to delete this team?")) {
            // Send AJAX request to delete team
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
