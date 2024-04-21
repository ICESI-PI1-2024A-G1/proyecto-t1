from itertools import chain
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import Http404, JsonResponse
from apps.forms.models import *
from apps.internalRequests.models import Traceability
import utils.utils as utils
from apps.teams.models import Team
from datetime import datetime
import math



@login_required
@csrf_exempt
def show_requests(request):
    """
    Show requests
    """
    advance_legalization = [obj.__dict__.update({'document': 'Legalización de Anticipos',
                                                 'initial_date': obj.request_date,
                                                 'fullname': obj.traveler_name,
                                                 'final_date': obj.final_date if obj.final_date else 'Por definir',
                                                 'manager': obj.member_name if obj.member_name else 'Por definir'}) or obj for obj in AdvanceLegalization.objects.all()]
    billing_account = [obj.__dict__.update({'document': 'Cuenta de Cobro',
                                            'initial_date': obj.request_date,
                                            'fullname': obj.full_name,
                                            'final_date': obj.final_date if obj.final_date else 'Por definir',
                                            'manager': obj.member_name if obj.member_name else 'Por definir'}) or obj for obj in BillingAccount.objects.all()]
    requisition = [obj.__dict__.update({'document': 'Requisición',
                                        'initial_date': obj.request_date,
                                        'fullname': obj.requester_name,
                                        'final_date': obj.final_date if obj.final_date else 'Por definir',
                                        'manager': obj.member_name if obj.member_name else 'Por definir'}) or obj for obj in Requisition.objects.all()]
    travel_advance_request = [obj.__dict__.update({'document': 'Solicitud de Viaje',
                                                   'initial_date': obj.request_date,
                                                   'fullname': obj.traveler_name,
                                                   'final_date': obj.final_date if obj.final_date else 'Por definir',
                                                   'manager': obj.member_name if obj.member_name else 'Por definir'}) or obj for obj in TravelAdvanceRequest.objects.all()]
    travel_expense_request = [obj.__dict__.update({'document': 'Legalización de Gastos de Viaje',
                                                   'initial_date': obj.request_date,
                                                   'fullname': obj.traveler_name,
                                                   'final_date': obj.final_date if obj.final_date else 'Por definir',
                                                   'manager': obj.member_name if obj.member_name else 'Por definir'}) or obj for obj in TravelExpenseLegalization.objects.all()]
    
    requests_data = list(chain(advance_legalization, billing_account, requisition, travel_advance_request, travel_expense_request))
    
    return render(request, "show-internal-requests.html", {"requests": requests_data})


@csrf_exempt
@login_required
def change_status(request, id):
    """
    Allows users to change the status of a request.

    HTTP Methods:
    - GET: Renders a form to change the status of the request.
    - POST: Handles form submission, updates the status of the request, and records traceability.

    Dependencies:
    - Models: For accessing request data in the database.
    - Traceability: Model for recording changes in request status.
    - utils.utils.send_verification_email: Utility function to send notification emails.

    Parameters:
    - request: Django request object.
    - id: ID of the request to be updated.

    Returns:
    - JsonResponse: JSON response indicating the result of the operation.
    """
    def get_request_by_id(id):
        models = [TravelAdvanceRequest, AdvanceLegalization, BillingAccount, Requisition, TravelExpenseLegalization]
        for model in models:
            try:
                return model.objects.get(id=id)
            except model.DoesNotExist:
                continue
        raise Http404(f"Request with id {id} not found in any of the tables")
    
    if request.method == "GET":
        curr_request = get_request_by_id(id)
        status_options = ["EN REVISION", "PENDIENTE", "DEVUELTO", "RECHAZADO"]
        return render(request, "change-status.html", {"request": curr_request, "status_options": status_options})

    elif request.method == "POST":
        try:
            curr_request = get_request_by_id(id)
            new_status = request.POST.get("newStatus")
            new_reason = request.POST.get("reason")
            prev_status = curr_request.status
            curr_request.status = new_status
            team_id = curr_request.team_id
            
            Traceability.objects.create(
                modified_by=request.user,
                prev_state=prev_status,
                new_state=new_status,
                reason=new_reason,
                date=datetime.now(),
                request=id
            )
            
            if(not math.isnan(team_id)):
                team = Team.objects.filter(id=team_id)
                if(team.exists()):
                    utils.send_verification_email(
                        request,
                        f"Actualización del estado de la solicitud {curr_request.id}",
                        "Notificación Vía Sistema de Contabilidad | Universidad Icesi <contabilidad@icesi.edu.co>",
                        team[0].leader.email,
                        f"Hola, el usuario identificado como {request.user} del equipo {team[0]} ha cambiado el estado de la solicitud {curr_request.id}\nEstado Anterior:{prev_status}\nNuevo Estado: {new_status}\nMotivo: {new_reason}",
                    )
            curr_request.save()
            return JsonResponse(
                {
                    "message": f"El estado de la solicitud {id} ha sido actualizado correctamente."
                }
            )

        except Exception as e:
            return JsonResponse(
                {"error": f"No se pudo realizar la operación: {str(e)}"}, status=500
            )


'''
@login_required
def assign_request(request, request_id):
    """
    Allows users to assign a request to another user.

    HTTP Methods:
    - GET: Renders a form to select a user for assignment.
    - POST: Handles form submission, updates the request with the assigned user, and sends a notification email.

    Dependencies:
    - sharepoint_api: For retrieving and updating request data.
    - Team: Model for accessing team information.
    - utils.utils.send_verification_email: Utility function to send notification emails.

    Parameters:
    - request: Django request object.
    - request_id: ID of the request to be assigned.

    Returns:
    - redirect: Redirects to the requests page after assignment.
    """
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
'''
