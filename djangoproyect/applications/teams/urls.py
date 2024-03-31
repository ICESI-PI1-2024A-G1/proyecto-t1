from django.urls import path

from applications.teams import views


urlpatterns = [
    path("", views.show_teams),
    path(
        "delete-member/<int:team_id>/<int:member_id>/",
        views.delete_member,
        name="delete_member",
    ),
    path("add-member/<int:team_id>/", views.add_member, name="add_member"),
    path("add-team-form/", views.add_team, name="add_team"),
    path("delete/<int:team_id>/", views.delete_team, name="delete_team"),
    path("member-details/<int:id>", views.member_details, name="member_details"),
]
