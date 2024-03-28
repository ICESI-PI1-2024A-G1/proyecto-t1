from django.http import JsonResponse
from django.shortcuts import redirect, render
from applications.requests.models import Requests
from .models import Team
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .forms import TeamForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


User = get_user_model()


### TEAM VIEWS


@never_cache
@login_required
def show_teams(request):
    if request.user.is_staff:
        teams = Team.objects.all()
    else:
        teams = Team.objects.filter(leader_id=request.user.id)
    return render(request, "show-teams.html", {"teams": teams})


@never_cache
@login_required
def add_team(request):
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
    if request.method == "DELETE":
        team = get_object_or_404(Team, id=team_id)
        team.delete()
        return JsonResponse(
            {"message": f"El equipo {team_id} ha sido eliminado correctamente"}
        )


### MEMBERS VIEWS


@never_cache
@login_required
def show_members(request, id):
    if request.method == "GET":
        team = get_object_or_404(Team, pk=id)
        members = team.members.all()
        return render(request, "show-members.html", {"members": members})
