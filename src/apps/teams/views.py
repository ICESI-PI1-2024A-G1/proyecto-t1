from django.http import JsonResponse
from django.shortcuts import redirect, render
from apps.requests.models import Requests
from .models import Team
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .forms import TeamForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from api.sharepoint_api import SharePointAPI
import os
from django.conf import settings

EXCEL_FILE_PATH = os.path.join(
    settings.BASE_DIR,
    "static",
    "requests",
    "emulation",
    "requests_database.xlsx",
)

sharepoint_api = SharePointAPI(EXCEL_FILE_PATH)

User = get_user_model()


### TEAM VIEWS


@never_cache
@login_required
def show_teams(request):
    """
    View to display a list of teams based on user permissions.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: A rendered HTML template displaying teams.

    Notes:
        - If the user is staff, all teams are displayed.
        - If the user is not staff, only teams led by the user are displayed.
    """
    if request.user.is_staff:
        teams = Team.objects.all()
    else:
        teams = Team.objects.filter(leader_id=request.user.id)
    return render(request, "show-teams.html", {"teams": teams})


@never_cache
@login_required
def add_team(request):
    """
    View to add a new team.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: A rendered HTML template for adding a team.

    Notes:
        - GET request renders an empty form.
        - POST request processes form submission.
        - Redirects to the teams list on successful form submission.
    """
    if request.method == "GET":
        form = TeamForm()
        return render(request, "add-team.html", {"form": form})
    elif request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/teams/")
        else:
            return render(request, "add-team.html", {"form": form})


@never_cache
@login_required
def edit_team(request, team_id):
    """
    View to edit an existing team.

    Args:
        request (HttpRequest): The request object.
        team_id (int): The ID of the team to edit.

    Returns:
        HttpResponse: A rendered HTML template for editing a team.

    Notes:
        - GET request renders a form pre-filled with team data.
        - POST request processes form submission for editing.
        - Redirects to the teams list on successful form submission.
    """
    team = get_object_or_404(Team, pk=team_id)
    form = TeamForm(instance=team)
    if request.method == "GET":
        return render(request, "edit-team.html", {"form": form})
    elif request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect("/teams/")
        else:
            return render(request, "edit-team.html", {"form": form})


@never_cache
@login_required
def delete_team(request, team_id):
    """
    View to delete a team.

    Args:
        request (HttpRequest): The request object.
        team_id (int): The ID of the team to delete.

    Returns:
        JsonResponse: JSON response confirming team deletion.

    Notes:
        - Requires a DELETE request method.
        - Deletes the team and removes it from SharePoint API.
        - Returns a JSON message confirming successful deletion.
    """
    if request.method == "DELETE":
        team = get_object_or_404(Team, id=team_id)
        team.delete()
        sharepoint_api.remove_team(team_id)
        return JsonResponse(
            {"message": f"El equipo {team_id} ha sido eliminado correctamente"}
        )


### MEMBERS VIEWS


@never_cache
@login_required
def show_members(request, id):
    """
    View to display members of a team.

    Args:
        request (HttpRequest): The request object.
        id (int): The ID of the team whose members to display.

    Returns:
        HttpResponse: A rendered HTML template displaying team members.
    """
    if request.method == "GET":
        team = get_object_or_404(Team, pk=id)
        members = team.members.all()
        return render(request, "show-members.html", {"members": members})
