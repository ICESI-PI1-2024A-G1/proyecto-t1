from datetime import datetime
import json
import math
import os
import traceback
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from api.sharepoint_api import SharePointAPI
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib.auth import get_user_model
from applications.requests.models import Traceability
import utils.utils as utils

from applications.teams.models import Team

from django.conf import settings

sharepoint_api = SharePointAPI(settings.EXCEL_FILE_PATH)

User = get_user_model()


@csrf_exempt
@login_required
def change_status(request, id):
    if request.method == "GET":
        curr_request = sharepoint_api.get_request_by_id(id)
        curr_request_data = json.loads(curr_request.content)
        status_options = [
            "EN PROCESO",
            "APROBADO - CENCO",
            "RECHAZADO - CENCO",
            "APROBADO - DECANO",
            "RECHAZADO - DECANO",
            "PAGADO - CONTABILIDAD",
            "RECHAZADO - CONTABILIDAD",
            "CERRADO",
        ]
        return render(request, "change-status.html", {"request": curr_request_data, "status_options": status_options})
    elif request.method == "POST":
        try:
            curr_request = sharepoint_api.get_request_by_id(id)
            curr_request_data = json.loads(curr_request.content)
            new_status = request.POST.get("newStatus")
            new_reason = request.POST.get("reason")
            prev_status = curr_request_data["status"]
            curr_request_data["status"] = new_status
            team_id = curr_request_data["team"]
            Traceability.objects.create(
                modified_by = request.user,
                prev_state = prev_status,
                new_state = new_status,
                reason = new_reason,
                date = datetime.now(),
                request=id
            )

            if(not math.isnan(team_id)):
                team = Team.objects.filter(id=team_id)
                if(team.exists()):
                    utils.send_verification_email(
                        request,
                        f"Actualización del estado de la solicitud {curr_request_data["id"]}",
                        "Notificación Vía Sistema de Contabilidad | Universidad Icesi <contabilidad@icesi.edu.co>",
                        team[0].leader.email,
                        f"Hola, el usuario identificado como {request.user} del equipo {team[0]} ha cambiado el estado de la solicitud {curr_request_data["id"]}\nEstado Anterior:{prev_status}\nNuevo Estado: {new_status}\nMotivo: {new_reason}",
                    )
            response = sharepoint_api.update_data(id, curr_request_data)
            if response.status_code == 200:
                return JsonResponse(
                    {
                        "message": f"El estado de la solicitud {id} ha sido actualizado correctamente."
                    }
                )
            else:
                return JsonResponse(
                    {"error": f"No se pudo realizar la operación: {response}"}, status=500
                )

        except Exception as e:
            return JsonResponse(
                {"error": f"No se pudo realizar la operación: {str(e)}"}, status=500
            )

def search(request, query):
    try:
        results = sharepoint_api.search_data(query=query)

        if results.status_code == 200:
            return JsonResponse(json.loads(results.content), safe=False)
        else:
            raise Http404("El archivo Excel no está disponible")
    except Http404 as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        return JsonResponse(
            {"error": f"No se pudo realizar la operación: {str(e)}"}, status=500
        )


@never_cache
@login_required
def show_requests(request):
    try:
        response = sharepoint_api.get_all_requests()
        if response.status_code == 200:
            requests_data = json.loads(response.content)
            user_str = request.user.__str__()
            if not request.user.is_staff and not request.user.is_leader:
                requests_data = [ r for r in requests_data if r["manager"] == user_str ]
            for r in requests_data:
                r["team"] = "" if math.isnan(r["team"]) else int(r["team"])
            return render(request, "show-requests.html", {"requests": requests_data})
        else:
            raise Http404("No se pudieron cargar las solicitudes.")
    except Http404 as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse(
            {"error": f"No se pudo realizar la operación: {str(e)}"}, status=500
        )


@never_cache
@login_required
def detail_request(request, id):
    try:
        api_response = sharepoint_api.get_request_by_id(id)
        detail = json.loads(api_response.content)
        if api_response.status_code == 200:
            return render(
                request,
                "request-detail.html",
                {"request": detail},
            )
        else:
            raise Http404(f"No se encontró la solicitud con ID {id} en SharePointAPI.")
    except Http404 as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        return JsonResponse(
            {"error": f"No se pudo realizar la operación: {str(e)}"}, status=500
        )


@login_required
def assign_request(request, request_id):
    api_response = sharepoint_api.get_request_by_id(request_id)
    curr_request = json.loads(api_response.content)
    if request.method == "GET":
        teams = Team.objects.filter(leader=request.user)
        if len(teams):
            users = teams[0].members.all()
        else:
            users = []
        return render(
            request, "assign-request.html", {"users": users, "request": curr_request}
        )
    elif request.method == "POST":
        try:
            user_id = request.POST["user_id"]
            manager = get_object_or_404(User, pk=user_id)
            curr_request["manager"] = manager
            teams = Team.objects.filter(leader=request.user)
            team = teams[0].id if teams.exists() else ""
            curr_request["team"] = team
            sharepoint_api.update_data(request_id, curr_request)
            try:
                utils.send_verification_email(
                    request,
                    "Solicitud Asignada",
                    "Notificación Vía Sistema de Contabilidad | Universidad Icesi <contabilidad@icesi.edu.co>",
                    manager.email,
                    f"Hola, como miembro del equipo {teams[0].name}, el líder {manager.first_name} {manager.last_name} le ha asignado una nueva solicitud en el Sistema de Contabilidad",
                )
            except:
                print("El destino no se encontró")                
        except Exception as e:
            print(e)
        return redirect("/requests/")

@login_required
def show_traceability(request, request_id):
    traceability = Traceability.objects.filter(request=request_id)
    return render(request, "show-traceability.html", {"traceability":traceability})
