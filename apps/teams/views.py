from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Team
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .forms import TeamForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from api.sharepoint_api import SharePointAPI
import os
from django.contrib import messages
from django.conf import settings
from apps.internalRequests.views import get_all_requests

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
    teams = []
    team = None
    if request.user.is_superuser:
        teams = Team.objects.all()
        for team in teams:
            team.length = team.members.count()
    else:
        team = Team.objects.filter(leader_id=request.user.id)[0]
        return render(request, "team-details.html", {"team": team})
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
        members = []
        leaders = []
        form_types = list(settings.FORM_TYPES.copy().values())
        for team in Team.objects.all():
            form_type = team.typeForm
            form_types.remove(form_type)
        users = User.objects.all()
        team_leaders = [t.leader_id for t in Team.objects.all()]

        for user in users:
            if user.is_leader and user.id not in team_leaders:
                leaders.append(user)
            elif user.is_member:
                members.append(user)
        return render(
            request,
            "add-team.html",
            {"leaders": leaders, "members": members, "form_types": form_types},
        )
    elif request.method == "POST":

        try:
            items = request.POST.items()
            members = []
            for key, value in items:
                if key.startswith("member-") and value == "on":
                    member_id = key.split("-")[1]
                    member = get_object_or_404(User, pk=member_id)
                    members.append(member)

            leader = get_object_or_404(User, pk=request.POST.get("leader"))
            team = Team.objects.create(
                name=request.POST.get("name"),
                leader=leader,
                description=request.POST.get("description"),
                typeForm=request.POST.get("form_type"),
            )
            team.members.set(members)
            messages.success(request, "Equipo creado con éxito")
            return redirect("/teams/")
        except Exception as e:
            messages.error(request, "Error al crear el equipo")
            return redirect("/teams/add-team-form")


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
    if request.method == "GET":
        members = []
        leaders = []
        form_types = list(settings.FORM_TYPES.copy().values())
        team = get_object_or_404(Team, pk=team_id)
        for curr_team in Team.objects.all():
            form_type = curr_team.typeForm
            if form_type != team.typeForm:
                form_types.remove(form_type)
        users = User.objects.all()
        team_leaders = [t.leader_id for t in Team.objects.all()]
        for user in users:
            if user.id == team.leader.id:
                leaders.append(user)
                pass
            if user.is_leader and user.id not in team_leaders:
                leaders.append(user)
            elif user.is_member:
                members.append(user)
        return render(
            request,
            "edit-team.html",
            {
                "team": team,
                "leaders": leaders,
                "members": members,
                "form_types": form_types,
            },
        )
    elif request.method == "POST":

        try:
            items = request.POST.items()
            members = []
            for key, value in items:
                # print(key, value)
                if key.startswith("member-") and value == "on":
                    member_id = key.split("-")[1]
                    member = get_object_or_404(User, pk=member_id)
                    members.append(member)

            leader = get_object_or_404(User, pk=request.POST.get("leader"))
            team.leader = leader
            team.name = request.POST.get("name")
            team.description = request.POST.get("description")
            team.typeForm = request.POST.get("form_type")
            prev_members = team.members.all()
            requests = get_all_requests(team.typeForm)
            assigned_members = [r.member for r in requests]
            assigned_members_list = []
            for member in prev_members:
                if member not in members and member in assigned_members:
                    assigned_members_list.append(member)
            if len(assigned_members_list):
                messages.error(
                    request,
                    "Hay solicitudes pendientes de este equipo para los miembros: "
                    + ", ".join([m.__str__() for m in assigned_members_list]),
                )
                return redirect(f"/teams/edit-team/{team_id}")
            team.members.set(members)
            team.save()
            messages.success(request, "Equipo editado con éxito")
            return redirect("/teams/")
        except Exception as e:
            print(e)
            messages.error(request, "Error al crear el equipo")
            return redirect(f"/teams/edit-team/{team_id}/")


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
        requests = get_all_requests(team.typeForm)
        assigned_members = [r.member for r in requests]
        assigned_members_list = []
        # print(team.members.all())
        # print(assigned_members)
        for member in team.members.all():
            if member in assigned_members:
                assigned_members_list.append(member)

        if len(assigned_members_list):
            messages.error(
                request,
                "Error al editar el equipo: Hay solicitudes pendientes para los miembros: "
                + ", ".join([m.__str__() for m in assigned_members_list]),
            )
            # print("aa")
            return JsonResponse({"error": "Error al editar el equipo"}, status=400)

        team.delete()
        sharepoint_api.remove_team(team_id)
        messages.success(request, "Equipo eliminado con éxito")
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
