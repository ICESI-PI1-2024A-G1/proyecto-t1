from django.urls import path
from applications.teams import views


urlpatterns = [
    path("", views.show_teams),
    path("assign-requests/<int:id>/", views.assign_requests, name="assign_requests"),
    path("add-team-form/", views.add_team, name="add_team"),
    path("delete/<int:team_id>/", views.delete_team, name="delete_team"),
    path("edit-team/<int:team_id>/", views.edit_team, name="edit_team"),
]
