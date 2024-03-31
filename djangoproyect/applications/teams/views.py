from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Team
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import TeamForm


# Create your views here.
def show_teams(request):
    teams = Team.objects.all()
    return render(request, "show-teams.html", {"teams": teams})


def delete_member(request, team_id, member_id):
    team = Team.objects.get(id=team_id)
    team.members.remove(member_id)
    team.save()
    return JsonResponse(
        {"message": f"El miembro {member_id} ha sido eliminado correctamente"}
    )


def add_member(request, team_id):
    if request.method == "GET":
        team = get_object_or_404(Team, id=team_id)
        users = User.objects.exclude(id__in=team.members.all()).exclude(
            id=team.leader.id
        )
        users_data = [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
            }
            for user in users
        ]

        return JsonResponse(users_data, safe=False)
    elif request.method == "POST":
        team = get_object_or_404(Team, id=team_id)
        selected_users_ids = [
            int(user_id) for user_id in request.POST.getlist("users[]")
        ]
        team.members.add(*selected_users_ids)
        team.save()

        new_members = User.objects.filter(id__in=selected_users_ids)
        new_members_data = [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
            }
            for user in new_members
        ]

        return JsonResponse(
            {
                "message": "Miembros añadidos con éxito al equipo.",
                "users": new_members_data,
            }
        )


def add_team(request):
    if request.method == "GET":
        form = TeamForm()
        return render(request, "add-team.html", {"form": form})
    elif request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            return redirect("/teams")
        else:
            return render(request, "add-team.html", {"form": form})


def delete_team(request, team_id):
    if request.method == "DELETE":
        team = get_object_or_404(Team, id=team_id)
        team.delete()
        return JsonResponse(
            {"message": f"El equipo {team_id} ha sido eliminado correctamente"}
        )


def member_details(request, id):
    if request.method == "GET":
        member = get_object_or_404(User, pk=id)
        member_requests = (
            member.requests.all()
        )  # Obtener las solicitudes asociadas al miembro
        return render(
            request,
            "member-details.html",
            {"member": member, "member_requests": member_requests},
        )
