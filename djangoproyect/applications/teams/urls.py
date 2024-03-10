from django.urls import path

from applications.teams import views


urlpatterns = [
    path("", views.show_teams),
    path("delete-member/<int:team_id>/<int:member_id>", views.delete_member),
    path("add-member-form/<int:team_id>", views.add_member),
    path("add-team/", views.add_team),
    path("delete/<int:team_id>", views.delete_team),
]
