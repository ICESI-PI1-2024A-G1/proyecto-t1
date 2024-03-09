from django.http import JsonResponse
from django.shortcuts import render
from .models import Team
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


# Create your views here.
def show_teams(request):
    teams = Team.objects.all()
    return render(request, "show-teams.html", {"teams": teams})


def delete_member(request, team_id, member_id):
    team = Team.objects.get(id=team_id)
    team.members.remove(member_id)
    team.save()
    return JsonResponse({"message": f"El miembro {id} ha sido eliminado correctamente"})


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
