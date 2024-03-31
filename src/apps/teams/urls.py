"""
Request urls

This module defines URL patterns for the teams application.
"""

from django.urls import path
from apps.teams import views

app_name = "teams"

urlpatterns = [
    path("", views.show_teams, name="show_teams"),
    path("add-team-form/", views.add_team, name="add_team"),
    path("delete/<int:team_id>/", views.delete_team, name="delete_team"),
    path("edit-team/<int:team_id>/", views.edit_team, name="edit_team"),
    path("show-members/<int:id>", views.show_members, name="show_members"),
]
