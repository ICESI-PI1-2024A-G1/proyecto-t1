from itertools import chain
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from apps.forms.models import *
from apps.internalRequests.models import Traceability
import utils.utils as utils
from apps.teams.models import Team
from datetime import datetime
import math

statusMap = {
    "PENDIENTE": "secondary",
    "EN REVISIÓN": "info",
    "DEVUELTO": "warning",
    "RECHAZADO": "danger",
}

User = get_user_model()


# This function is used to get the request by its id
def get_request_by_id(id):
    models = [
        TravelAdvanceRequest,
        AdvanceLegalization,
        BillingAccount,
        Requisition,
        TravelExpenseLegalization,
    ]
    for model in models:
        try:
            return model.objects.get(id=id)
        except model.DoesNotExist:
            continue
    raise Http404(f"Request with id {id} not found in any of the tables")


@login_required
@csrf_exempt
def show_requests(request):
    """
    Show requests
    """
    if request.user.is_superuser or request.user.is_leader:
        if (
            request.user.is_superuser
            or request.user.is_leader
            and Team.objects.filter(leader_id=request.user.id).exists()
        ):
            advance_legalization = [
                obj.__dict__.update(
                    {
                        "document": "Legalización de Anticipos",
                        "initial_date": obj.request_date,
                        "fullname": obj.traveler_name,
                        "final_date": (
                            obj.final_date if obj.final_date else "Por definir"
                        ),
                        "manager": (
                            obj.member_name if obj.member_name else "Por definir"
                        ),
                    }
                )
                or obj
                for obj in AdvanceLegalization.objects.all()
            ]
            billing_account = [
                obj.__dict__.update(
                    {
                        "document": "Cuenta de Cobro",
                        "initial_date": obj.request_date,
                        "fullname": obj.full_name,
                        "final_date": (
                            obj.final_date if obj.final_date else "Por definir"
                        ),
                        "manager": (
                            obj.member_name if obj.member_name else "Por definir"
                        ),
                    }
                )
                or obj
                for obj in BillingAccount.objects.all()
            ]
            requisition = [
                obj.__dict__.update(
                    {
                        "document": "Requisición",
                        "initial_date": obj.request_date,
                        "fullname": obj.requester_name,
                        "final_date": (
                            obj.final_date if obj.final_date else "Por definir"
                        ),
                        "manager": (
                            obj.member_name if obj.member_name else "Por definir"
                        ),
                    }
                )
                or obj
                for obj in Requisition.objects.all()
            ]
            travel_advance_request = [
                obj.__dict__.update(
                    {
                        "document": "Solicitud de Viaje",
                        "initial_date": obj.request_date,
                        "fullname": obj.traveler_name,
                        "final_date": (
                            obj.final_date if obj.final_date else "Por definir"
                        ),
                        "manager": (
                            obj.member_name if obj.member_name else "Por definir"
                        ),
                    }
                )
                or obj
                for obj in TravelAdvanceRequest.objects.all()
            ]
            travel_expense_request = [
                obj.__dict__.update(
                    {
                        "document": "Legalización de Gastos de Viaje",
                        "initial_date": obj.request_date,
                        "fullname": obj.traveler_name,
                        "final_date": (
                            obj.final_date if obj.final_date else "Por definir"
                        ),
                        "manager": (
                            obj.member_name if obj.member_name else "Por definir"
                        ),
                    }
                )
                or obj
                for obj in TravelExpenseLegalization.objects.all()
            ]
        else:
            return render(
                request, "show-internal-requests.html", {"no_permission": True}
            )
    else:
        advance_legalization = [
            obj.__dict__.update(
                {
                    "document": "Legalización de Anticipos",
                    "initial_date": obj.request_date,
                    "fullname": obj.traveler_name,
                    "final_date": obj.final_date if obj.final_date else "Por definir",
                    "manager": obj.member_name if obj.member_name else "Por definir",
                }
            )
            or obj
            for obj in AdvanceLegalization.objects.filter(id_person=request.user.id)
        ]
        billing_account = [
            obj.__dict__.update(
                {
                    "document": "Cuenta de Cobro",
                    "initial_date": obj.request_date,
                    "fullname": obj.full_name,
                    "final_date": obj.final_date if obj.final_date else "Por definir",
                    "manager": obj.member_name if obj.member_name else "Por definir",
                }
            )
            or obj
            for obj in BillingAccount.objects.filter(id_person=request.user.id)
        ]
        requisition = [
            obj.__dict__.update(
                {
                    "document": "Requisición",
                    "initial_date": obj.request_date,
                    "fullname": obj.requester_name,
                    "final_date": obj.final_date if obj.final_date else "Por definir",
                    "manager": obj.member_name if obj.member_name else "Por definir",
                }
            )
            or obj
            for obj in Requisition.objects.filter(id_person=request.user.id)
        ]
        travel_advance_request = [
            obj.__dict__.update(
                {
                    "document": "Solicitud de Viaje",
                    "initial_date": obj.request_date,
                    "fullname": obj.traveler_name,
                    "final_date": obj.final_date if obj.final_date else "Por definir",
                    "manager": obj.member_name if obj.member_name else "Por definir",
                }
            )
            or obj
            for obj in TravelAdvanceRequest.objects.filter(id_person=request.user.id)
        ]
        travel_expense_request = [
            obj.__dict__.update(
                {
                    "document": "Legalización de Gastos de Viaje",
                    "initial_date": obj.request_date,
                    "fullname": obj.traveler_name,
                    "final_date": obj.final_date if obj.final_date else "Por definir",
                    "manager": obj.member_name if obj.member_name else "Por definir",
                }
            )
            or obj
            for obj in TravelExpenseLegalization.objects.filter(
                id_person=request.user.id
            )
        ]

    requests_data = list(
        chain(
            advance_legalization,
            billing_account,
            requisition,
            travel_advance_request,
            travel_expense_request,
        )
    )

    for r in requests_data:
        r.status_color = statusMap[r.status]

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
    if request.method == "GET":
        curr_request = get_request_by_id(id)
        status_options = ["EN REVISIÓN", "PENDIENTE", "DEVUELTO", "RECHAZADO"]
        return render(
            request,
            "change-status.html",
            {"request": curr_request, "status_options": status_options},
        )

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
                request=id,
            )

            if not math.isnan(team_id):
                team = Team.objects.filter(id=team_id)
                if team.exists():
                    if request.user.is_superuser:
                        utils.send_verification_email(
                            request,
                            f"Actualización del estado de la solicitud {curr_request.id}",
                            "Notificación Vía Sistema de Contabilidad | Universidad Icesi <contabilidad@icesi.edu.co>",
                            team[0].leader.email,
                            f"Hola, el Administrador del Sistema ha cambiado el estado de la solicitud {curr_request.id}\nEstado Anterior:{prev_status}\nNuevo Estado: {new_status}\nMotivo: {new_reason}",
                        )
                    else:
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


@never_cache
@csrf_exempt
@login_required
def detail_request(request, id):
    """
    Renders a page displaying details of a specific request.

    HTTP Method:
    - GET

    Dependencies:
    - requests.models: For accessing request data in the database.

    Parameters:
    - request: Django request object.
    - id: ID of the request to be displayed.

    Returns:
    - render: Renders the HTML template with request details.
    """
    request_data = get_request_by_id(id)
    context = {"request": request_data}

    # Use the request type to determine which template to render
    if isinstance(request_data, AdvanceLegalization):
        expenses = AdvanceLegalization_Table.objects.filter(
            general_data_id=request_data.id
        )
        context["expenses"] = expenses
        return render(request, "forms/advance_legalization.html", context)
    elif isinstance(request_data, BillingAccount):
        context["include_cex"] = True
        return render(request, "forms/billing_account.html", context)
    elif isinstance(request_data, Requisition):
        return render(request, "forms/requisition.html", context)
    elif isinstance(request_data, TravelAdvanceRequest):
        expenses = json.loads(request_data.expenses)
        context["expenses"] = expenses
        return render(request, "forms/travel_advance_request.html", context)
    elif isinstance(request_data, TravelExpenseLegalization):
        expenses = TravelExpenseLegalization_Table.objects.filter(
            travel_info_id=request_data.id
        )
        context["expenses"] = expenses
        return render(request, "forms/travel_expense_legalization.html", context)
    else:
        return render(request, "forms/default_form.html", context)


@csrf_exempt
@login_required
def show_traceability(request, request_id):
    """
    Renders a page displaying the traceability of a specific request.

    HTTP Method:
    - GET

    Dependencies:
    - Traceability: Model for accessing traceability information.

    Parameters:
    - request: Django request object.
    - request_id: ID of the request for which traceability is to be displayed.

    Returns:
    - render: Renders the HTML template with traceability information.
    """
    traceability = Traceability.objects.filter(request=request_id)
    for t in traceability:
        t.prev_color = statusMap[t.prev_state]
        t.new_color = statusMap[t.new_state]
    traceability = traceability[::-1]
    return render(request, "show-traceability.html", {"traceability": traceability})


@csrf_exempt
@login_required
def assign_request(request, request_id):
    """
    Allows users to assign a request to another user.

    HTTP Methods:
    - GET: Renders a form to select a user for assignment.
    - POST: Handles form submission, updates the request with the assigned user, and sends a notification email.

    Dependencies:
    - Team: Model for accessing team information.
    - utils.utils.send_verification_email: Utility function to send notification emails.

    Parameters:
    - request: Django request object.
    - request_id: ID of the request to be assigned.

    Returns:
    - redirect: Redirects to the requests page after assignment.
    """
    curr_request = get_request_by_id(request_id)
    if isinstance(curr_request, AdvanceLegalization):
        form_type = "Legalización de Anticipos"
    elif isinstance(curr_request, BillingAccount):
        form_type = "Cuenta de Cobro"
    elif isinstance(curr_request, Requisition):
        form_type = "Requisición"
    elif isinstance(curr_request, TravelAdvanceRequest):
        form_type = "Solicitud de Viaje"
    elif isinstance(curr_request, TravelExpenseLegalization):
        form_type = "Legalización de Gastos de Viaje"
    else:
        form_type = None

    if request.method == "GET":
        if form_type is not None:
            teams = Team.objects.filter(typeForm=form_type)
            if len(teams):
                users = teams[0].members.all()
            else:
                users = []
        else:
            users = []

        return render(
            request, "assign-request.html", {"users": users, "request": curr_request}
        )
    elif request.method == "POST":
        try:
            user_id = request.POST["user_id"]
            manager = get_object_or_404(User, pk=user_id)
            curr_request.member_name = manager.first_name + " " + manager.last_name
            curr_request.save()
            teams = Team.objects.filter(typeForm=form_type)
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
        messages.success(request, "La solicitud ha sido asignada exitosamente.")
        return redirect("/requests/")
