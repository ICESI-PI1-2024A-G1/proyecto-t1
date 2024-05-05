from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from apps.forms.models import *
from apps.internalRequests.models import Traceability
from apps.requests.models import SharePoint
from apps.teams.models import Team
import utils.utils as utils
from datetime import datetime
from django.db import transaction
from django.template.loader import get_template
import json
import os
from django.conf import settings
import random
from datetime import datetime
import re
from weasyprint import HTML
import tempfile

statusMap = {
    "PENDIENTE": "secondary",
    "EN REVISIÓN": "info",
    "POR APROBAR": "primary",
    "DEVUELTO": "warning",
    "RECHAZADO": "danger",
    "RESUELTO": "success",
}

User = get_user_model()


# Get cities with countries
def get_cities_with_countries():
    cities_with_countries = (
        City.objects.select_related("country").order_by("country_id").all()
    )

    cities_data = [
        {
            "city_id": city.id,
            "city_name": city.name,
            "country_name": city.country.name,
            "country_code": city.country.code,
        }
        for city in cities_with_countries
    ]

    return cities_data


# Get bank data
def get_bank_data():
    banks = Bank.objects.all()

    bank_data = [
        {
            "bank_id": bank.id,
            "bank_name": bank.name,
        }
        for bank in banks
    ]

    return bank_data


# Get account types
def get_account_types():
    account_types = AccountType.objects.all()

    account_types = [
        {
            "account_type_id": account_type.id,
            "account_type_name": account_type.name,
        }
        for account_type in account_types
    ]

    return account_types


# Get dependence data
def get_dependence_data():
    dependences = Dependency.objects.all()

    dependence_data = [
        {
            "dependence_id": dependence.id,
            "dependence_name": dependence.name,
        }
        for dependence in dependences
    ]

    return dependence_data


# Get cost center data
def get_cost_center_data():
    cost_centers = CostCenter.objects.all()

    cost_center_data = [
        {
            "cost_center_id": cost_center.id,
            "cost_center_name": cost_center.name,
        }
        for cost_center in cost_centers
    ]

    return cost_center_data


# Create context for the form
def create_context():
    cities_data = get_cities_with_countries()
    bank_data = get_bank_data()
    account_types = get_account_types()
    dependences = get_dependence_data()
    cost_centers = get_cost_center_data()

    context = {
        "cities": cities_data,
        "banks": bank_data,
        "account_types": account_types,
        "dependences": dependences,
        "cost_centers": cost_centers,
    }

    return context


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


def get_all_requests(formType=None):
    models = [
        TravelAdvanceRequest,
        AdvanceLegalization,
        BillingAccount,
        Requisition,
        TravelExpenseLegalization,
    ]
    if formType:
        models = [
            model for model in models if formType == settings.FORM_TYPES[model.__name__]
        ]
    instances = []
    for model in models:
        for instance in model.objects.all():
            instance.document = settings.FORM_TYPES[model.__name__]
            instances.append(instance)
    return instances


@never_cache
@login_required
@csrf_exempt
def show_requests(request):
    """
    Show requests
    """
    message = None
    message_type = None

    if "changeStatusDone" in request.GET:
        message = "El estado de la solicitud ha sido actualizado correctamente."
        message_type = messages.SUCCESS
    elif "changeStatusFailed" in request.GET:
        message = "No se pudo realizar la operación."
        message_type = messages.ERROR
    elif "fixRequestDone" in request.GET:
        message = "El formulario ha sido enviado para revisión."
        message_type = messages.SUCCESS
    elif "fixRequestFailed" in request.GET:
        message = "No se pudo enviar el formulario para revisión."
        message_type = messages.ERROR
    elif "reviewDone" in request.GET:
        message = "El formulario ha sido revisado."
        message_type = messages.SUCCESS
    elif "changeFinalDateDone" in request.GET:
        message = "La fecha final de la solicitud ha sido actualizada correctamente."
        message_type = messages.SUCCESS
    elif "changeFinalDateFailed" in request.GET:
        message = "No se pudo actualizar la fecha final de la solicitud."
        message_type = messages.ERROR

    requests_data = get_all_requests()
    print(request.user.is_leader)
    if request.user.is_leader:
        if Team.objects.filter(leader_id=request.user.id).exists():
            team = Team.objects.get(leader_id=request.user.id)

            requests_data = list(
                filter(
                    lambda x: x.document and x.document == team.typeForm,
                    requests_data,
                )
            )
        else:
            return render(
                request, "show-internal-requests.html", {"no_permission": True}
            )
    if request.user.is_member:
        requests_data = list(
            filter(
                lambda x: x.member and x.member.id == request.user.id,
                requests_data,
            )
        )
    if request.user.is_applicant:
        requests_data = list(
            filter(
                lambda x: x.id_person and x.id_person == request.user.id,
                requests_data,
            )
        )

    for r in requests_data:
        r.status_color = statusMap[r.status]

    requests_data = sorted(requests_data, key=lambda x: x.request_date, reverse=True)

    if message and message_type:
        messages.add_message(request, message_type, message)
        return redirect("/requests")

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
        if curr_request.status == "PENDIENTE":
            status_options = ["EN REVISIÓN"]
            return render(
                request,
                "change-status.html",
                {"request": curr_request, "status_options": status_options},
            )
        elif curr_request.status == "POR APROBAR":
            status_options = ["RESUELTO", "DEVUELTO", "RECHAZADO"]
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

            if team_id:
                print(team_id.leader)
                print(team_id.leader.email)
                if request.user.is_superuser:
                    utils.send_verification_email(
                        request,
                        f"Actualización del estado de la solicitud {curr_request.id}",
                        "Notificación Vía Sistema de Contabilidad | Universidad Icesi <contabilidad@icesi.edu.co>",
                        team_id.leader.email,
                        f"Hola, el Administrador del Sistema ha cambiado el estado de la solicitud {curr_request.id}\nEstado Anterior:{prev_status}\nNuevo Estado: {new_status}\nMotivo: {new_reason}",
                    )
                else:
                    utils.send_verification_email(
                        request,
                        f"Actualización del estado de la solicitud {curr_request.id}",
                        "Notificación Vía Sistema de Contabilidad | Universidad Icesi <contabilidad@icesi.edu.co>",
                        team_id.leader.email,
                        f"Hola, el usuario identificado como {request.user} del equipo {team_id} ha cambiado el estado de la solicitud {curr_request.id}\nEstado Anterior:{prev_status}\nNuevo Estado: {new_status}\nMotivo: {new_reason}",
                    )

            if curr_request.status == "POR APROBAR":
                # Put info of curr_request in a PDF
                if isinstance(curr_request, AdvanceLegalization):
                    html_file_path = "forms/advance_legalization.html"
                    document = "Legalización de Anticipos"
                elif isinstance(curr_request, BillingAccount):
                    html_file_path = "forms/billing_account.html"
                    document = "Cuenta de Cobro"
                elif isinstance(curr_request, Requisition):
                    html_file_path = "forms/requisition.html"
                    document = "Requisición"
                elif isinstance(curr_request, TravelAdvanceRequest):
                    html_file_path = "forms/travel_advance_request.html"
                    document = "Solicitud de Viaje"
                elif isinstance(curr_request, TravelExpenseLegalization):
                    html_file_path = "forms/travel_expense_legalization.html"
                    document = "Legalización de Gastos de Viaje"
                else:
                    form_type = None

                try:
                    detail_request(request, id, pdf=True)
                except Exception as e:
                    print(e)
                faculty = [
                    "Ciencias Administrativas y económicas",
                    "Ingeniería, Diseño y Ciencias Aplicadas",
                    "Ciencias Humanas",
                    "Ciencias de la Salud",
                ]
                eps = [
                    "Sura",
                    "Sanitas",
                    "Famisanar",
                    "Compensar",
                    "Medimás",
                    "Salud Total",
                    "Coomeva",
                    "Nueva EPS",
                    "Aliansalud",
                    "SOS",
                    "Cafesalud",
                    "Coosalud",
                    "Savia Salud",
                    "Mutual Ser",
                    "Cruz Blanca",
                    "Capital Salud",
                    "Comfenalco",
                    "Comfama",
                    "Comfandi",
                    "Comfasucre",
                ]
                pension_fund = [
                    "Porvenir",
                    "Protección",
                    "Colfondos",
                    "Skandia",
                    "Old Mutual",
                    "Colpensiones",
                    "Habitat",
                    "Horizonte",
                    "Crecer",
                    "Fiduprevisora",
                    "Cafam",
                    "Confuturo",
                    "CFA",
                    "Fondo Nacional del Ahorro",
                ]

                status_options = [
                    "EN PROCESO",
                    "APROBADO - CENCO",
                    "RECHAZADO - CENCO",
                    "APROBADO - DECANO",
                    "RECHAZADO - DECANO",
                    "PAGADO - CONTABILIDAD",
                    "RECHAZADO - CONTABILIDAD",
                ]

                arls = [
                    "Sura ARL",
                    "Positiva ARL",
                    "Colmena Seguros ARL",
                    "Seguros Bolívar ARL",
                    "Axa Colpatria ARL",
                    "Liberty Seguros ARL",
                    "Bolívar ARL",
                    "Mapfre ARL",
                    "Equidad Seguros ARL",
                    "Seguros del Estado ARL",
                    "Mundial de Seguros ARL",
                    "La Previsora ARL",
                    "Seguros Generales Suramericana ARL",
                    "Seguros del Sur ARL",
                    "Protección ARL",
                ]

                if hasattr(curr_request, "fullname"):
                    fullname = curr_request.fullname
                else:
                    fullname = "No aplica"

                if hasattr(curr_request, "cost_center"):
                    cenco = curr_request.cost_center
                elif hasattr(curr_request, "CENCO"):
                    cenco = curr_request.cenco
                else:
                    cenco = "No aplica"

                SharePoint.objects.create(
                    status=random.choice(status_options),
                    manager=curr_request.member,
                    team=curr_request.team_id.id if curr_request.team_id else None,
                    initial_date=datetime.now(),
                    final_date=datetime.now(),
                    fullname=fullname,
                    faculty=random.choice(faculty),
                    document=document,
                    phone_number=random.randint(1000000, 9999999),
                    email=User.objects.get(id=curr_request.id_person).email,
                    CENCO=cenco,
                    bank=curr_request.bank,
                    account_type=curr_request.account_type,
                    health_provider=random.choice(eps),
                    pension_fund=random.choice(pension_fund),
                    arl=random.choice(arls),
                    contract_value=random.randint(
                        100000, 10000000
                    ),  # Random value between 100,000 and 10,000,000
                    is_one_time_payment=random.choice([True, False]),
                )
            # if curr_request.status in ["DEVUELTO", "RECHAZADO", "RESUELTO"]:
            #     curr_request.member = None
            curr_request.save()
            return JsonResponse(
                {
                    "message": f"El estado de la solicitud {id} ha sido actualizado correctamente."
                }
            )

        except Exception as e:
            print(e)
            return JsonResponse(
                {"error": f"No se pudo realizar la operación: {str(e)}"}, status=500
            )


@csrf_exempt
@login_required
def change_final_date(request, id):
    """
    Allows users to change the final date of a request.

    HTTP Methods:
    - GET: Renders a form to change the final date of the request.
    - POST: Handles form submission, updates the final date of the request, and records traceability.

    Dependencies:
    - Models: For accessing request data in the database.
    - Traceability: Model for recording changes in request status.

    Parameters:
    - request: Django request object.
    - id: ID of the request to be updated.

    Returns:
    - JsonResponse: JSON response indicating the result of the operation.
    """
    if request.method == "GET":
        curr_request = get_request_by_id(id)
        curr_request.final_date = curr_request.final_date.strftime("%Y-%m-%d")
        return render(request, "change-date.html", {"request": curr_request})
    elif request.method == "POST":
        try:
            curr_request = get_request_by_id(id)
            new_final_date_str = request.POST.get("newFinalDate")
            reason = request.POST.get("reason")
            prev_state = curr_request.status
            prev_date = curr_request.final_date
            curr_request.final_date = new_final_date_str
            curr_request.save()

            # Convertir new_final_date a un objeto datetime.date
            new_final_date = datetime.strptime(new_final_date_str, "%Y-%m-%d").date()

            Traceability.objects.create(
                modified_by=request.user,
                prev_state=prev_state,
                new_state=prev_state,
                reason="Hubo un cambio de fecha: "
                + prev_date.strftime("%Y-%m-%d")
                + " -> "
                + new_final_date.strftime("%Y-%m-%d")
                + ".<br>Motivo: "
                + reason,
                date=datetime.now(),
                request=id,
            )

            return JsonResponse(
                {
                    "message": f"La fecha final de la solicitud {id} ha sido actualizada correctamente."
                }
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {"error": f"No se pudo realizar la operación: {str(e)}"}, status=500
            )


@never_cache
@csrf_exempt
@login_required
def detail_request(request, id, pdf=False, save_to_file=False):
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

    # Obtain bank, account type, city, dependence, and cost center data
    context.update(create_context())

    # Use the request type to determine which template to render
    if isinstance(request_data, AdvanceLegalization):
        expenses = AdvanceLegalization_Table.objects.filter(
            general_data_id=request_data.id
        )
        context["expenses"] = expenses
        template = "forms/advance_legalization.html"
    elif isinstance(request_data, BillingAccount):
        context["include_cex"] = True
        template = "forms/billing_account.html"
    elif isinstance(request_data, Requisition):
        template = "forms/requisition.html"
    elif isinstance(request_data, TravelAdvanceRequest):
        expenses = json.loads(request_data.expenses)
        context["expenses"] = expenses
        template = "forms/travel_advance_request.html"
    elif isinstance(request_data, TravelExpenseLegalization):
        expenses = TravelExpenseLegalization_Table.objects.filter(
            travel_info_id=request_data.id
        )
        context["expenses"] = expenses
        template = "forms/travel_expense_legalization.html"
    else:
        template = "forms/default_form.html"

    if request_data.status == "DEVUELTO" and request.user.is_applicant:
        context["editable"] = True
    if (
        request.user.is_member and request.user.is_leader
    ) and request_data.status == "EN REVISIÓN":
        context["canReview"] = True

    if pdf:
        context["pdf"] = True
        context["user"] = request.user
        context["user"].is_applicant = True
        css_file_path = os.path.join(
            settings.BASE_DIR, "static", "general", "css", "bootstrap.css"
        )
        template = get_template(template)
        html = template.render(context)
        if save_to_file:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                out_pdf = tmp_file.name
                # Convierte la plantilla HTML en PDF usando weasyprint
                pdf_bytes = HTML(string=html).write_pdf(
                    out_pdf, stylesheets=[css_file_path], presentational_hints=True
                )
                # Lee el PDF generado y envíalo como respuesta HTTP
                with open(out_pdf, "rb") as pdf_file:
                    response = HttpResponse(
                        pdf_file.read(), content_type="application/pdf"
                    )
                    response["Content-Disposition"] = (
                        'attachment; filename="archivo.pdf"'
                    )
                    return response
        else:
            pdf_bytes = HTML(string=html).write_pdf(
                stylesheets=[css_file_path], presentational_hints=True
            )
            addresses = ["ccsa101010@gmail.com"]
            try:
                leader_email = Team.objects.get(
                    typeForm=settings.FORM_TYPES[request_data.__class__.__name__]
                ).leader.email
                print(leader_email)
                addresses.append(leader_email)
            except:
                pass

            utils.send_verification_email(
                request,
                f"Archivo para revisión de la solicitud {id}",
                "Notificación Vía Sistema de Contabilidad | Universidad Icesi <contabilidad@icesi.edu.co>",
                addresses,
                f"Hola, el equipo de Contabilidad de la Universidad Icesi te envía el siguiente archivo para ser revisado. Este archivo contiene detalles de la solicitud {id} que ha sido actualizada recientemente. Por favor, revisa el archivo adjunto y haznos saber si tienes alguna pregunta o necesitas más información. Gracias por tu atención a este asunto.",
                pdf_bytes,
            )
    else:
        # Renderizar la plantilla HTML normalmente
        return render(request, template, context)


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
    traceability = sorted(traceability, key=lambda x: x.date, reverse=True)
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

    print(form_type)
    if request.method == "GET":
        if form_type is not None:
            teams = Team.objects.filter(leader=request.user)
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
            if user_id == "unassigned":
                curr_request.member = None
                curr_request.save()
                messages.success(
                    request, "La solicitud ha sido desasignada correctamente."
                )
                return redirect("/requests/?assignRequestDone")
            manager = get_object_or_404(User, pk=user_id)
            curr_request.member = manager
            curr_request.team_id = Team.objects.get(leader=request.user)
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
            return redirect("/requests/?assignRequestDone")
        except Exception as e:
            print(e)


@csrf_exempt
@login_required
def travel_advance_request(request):
    """
    Review the travel advance request form.

    HTTP Method:
    - POST

    Returns:
    - render: Changes status of the request to reviewed.
    """
    request_id = request.POST.get("id")
    review_data = request.POST.dict()
    request = TravelAdvanceRequest.objects.get(id=request_id)

    # Mapping of field names to data-message
    field_to_message = {
        "dateCheck": "Fecha",
        "nameCheck": "Nombre",
        "idCheck": "ID",
        "dependenceCheck": "Dependencia",
        "costsCheck": "Costos",
        "destinationCheck": "Destino",
        "startTravelCheck": "Inicio del viaje",
        "endTravelCheck": "Fin del viaje",
        "travelReasonCheck": "Razón del viaje",
        "tableCheck": "Tabla",
        "signCheck": "Firma",
        "bankCheck": "Banco",
        "typeAccountCheck": "Tipo de cuenta",
        "idBankCheck": "ID del banco",
        "observationsCheck": "Observaciones",
        "reasonData": "Razón",
    }

    # Initialize review_data_list with all checkboxes with a value of 'off'
    review_data_list = [
        {"id": key, "message": field_to_message.get(key, ""), "value": "off"}
        for key in field_to_message.keys()
    ]

    # Update the values of the checkboxes that are checked
    for item in review_data_list:
        if item["id"] in review_data:
            item["value"] = review_data[item["id"]]

    request.review_data = review_data_list
    request.is_reviewed = True
    request.save()

    return redirect("/requests/?reviewDone")


@csrf_exempt
@login_required
def travel_expense_legalization(request):
    """
    Review the travel expense legalization form.

    HTTP Method:
    - POST

    Returns:
    - render: Changes status of the request to reviewed.
    """
    request_id = request.POST.get("id")
    review_data = request.POST.dict()
    request = TravelExpenseLegalization.objects.get(id=request_id)

    # Mapping of field names to data-message
    field_to_message = {
        "dateCheck": "Fecha",
        "nameCheck": "Nombre",
        "idCheck": "ID",
        "dependenceCheck": "Dependencia",
        "costsCheck": "Costos",
        "destinationCheck": "Destino",
        "startTravelCheck": "Inicio de viaje",
        "endTravelCheck": "Fin de viaje",
        "travelReasonCheck": "Razón de viaje",
        "tableCheck": "Tabla",
        "signCheck": "Firma",
        "bankCheck": "Banco",
        "typeAccountCheck": "Tipo de cuenta",
        "idBankCheck": "ID del banco",
        "observationsCheck": "Observaciones",
        "reasonData": "Razón",
    }

    # Initialize review_data_list with all checkboxes with a value of 'off'
    review_data_list = [
        {"id": key, "message": field_to_message.get(key, ""), "value": "off"}
        for key in field_to_message.keys()
    ]

    # Update the values of the checkboxes that are checked
    for item in review_data_list:
        if item["id"] in review_data:
            item["value"] = review_data[item["id"]]

    request.review_data = review_data_list
    request.is_reviewed = True
    request.save()

    return redirect("/requests/?reviewDone")


@csrf_exempt
@login_required
def advance_legalization(request):
    """
    Review the advance legalization form.

    HTTP Method:
    - POST

    Returns:
    - render: Changes status of the request to reviewed.
    """
    request_id = request.POST.get("id")
    review_data = request.POST.dict()
    request = AdvanceLegalization.objects.get(id=request_id)

    # Mapping of field names to data-message
    field_to_message = {
        "dateCheck": "Fecha",
        "nameCheck": "Nombre",
        "idCheck": "ID",
        "dependenceCheck": "Dependencia",
        "costsCheck": "Costos",
        "purchaseReasonCheck": "Razón de compra",
        "tableCheck": "Tabla",
        "signCheck": "Firma",
        "bankCheck": "Banco",
        "typeAccountCheck": "Tipo de cuenta",
        "idBankCheck": "ID del banco",
        "observationsCheck": "Observaciones",
        "reasonData": "Razón",
    }

    # Inicializar review_data_list con todos los checkboxes con un valor de 'off'
    review_data_list = [
        {"id": key, "message": field_to_message.get(key, ""), "value": "off"}
        for key in field_to_message.keys()
    ]

    # Actualizar los valores de los checkboxes que están marcados
    for item in review_data_list:
        if item["id"] in review_data:
            item["value"] = review_data[item["id"]]

    request.review_data = review_data_list
    request.is_reviewed = True
    request.save()

    return redirect("/requests/?reviewDone")


@csrf_exempt
@login_required
def billing_account(request):
    """
    Review the billing account form.

    HTTP Method:
    - POST

    Returns:
    - render: Changes status of the request to reviewed.
    """
    request_id = request.POST.get("id")
    review_data = request.POST.dict()
    request = BillingAccount.objects.get(id=request_id)

    # Mapping of field names to data-message
    field_to_message = {
        "dateCheck": "Fecha",
        "nameCheck": "Nombre",
        "idCheck": "ID",
        "valueCheck": "Valor",
        "conceptCheck": "Concepto",
        "retentionCheck": "Retención",
        "taxCheck": "Impuesto",
        "residentCheck": "Residente",
        "cityCheck": "Ciudad",
        "addressCheck": "Dirección",
        "cellphoneCheck": "Celular",
        "signCheck": "Firma",
        "bankCheck": "Banco",
        "typeAccountCheck": "Tipo de cuenta",
        "idBankCheck": "ID del banco",
        "cexCheck": "CEX",
        "reasonData": "Razón",
    }

    # Initialize review_data_list with all checkboxes with a value of 'off'
    review_data_list = [
        {"id": key, "message": field_to_message.get(key, ""), "value": "off"}
        for key in field_to_message.keys()
    ]

    # Update the values of the checkboxes that are checked
    for item in review_data_list:
        if item["id"] in review_data:
            item["value"] = review_data[item["id"]]

    request.review_data = review_data_list
    request.is_reviewed = True
    request.save()

    return redirect("/requests/?reviewDone")


@csrf_exempt
@login_required
def requisition(request):
    """
    Review the requisition form.

    HTTP Method:
    - POST

    Returns:
    - render: Changes status of the request to reviewed.
    """
    request_id = request.POST.get("id")
    review_data = request.POST.dict()
    request = Requisition.objects.get(id=request_id)

    # Mapeo de los nombres de los campos a los data-message
    field_to_message = {
        "dateCheck": "Fecha",
        "nameCheck": "Nombre",
        "idCheck": "ID",
        "workCheck": "Trabajo",
        "dependenceCheck": "Dependencia",
        "cencoCheck": "Cenco",
        "valueCheck": "Valor",
        "conceptCheck": "Concepto",
        "descriptionCheck": "Descripción",
        "signCheck": "Firma",
        "bankCheck": "Banco",
        "typeAccountCheck": "Tipo de cuenta",
        "idBankCheck": "ID del banco",
        "observationsCheck": "Observaciones",
        "reasonData": "Razón",
    }

    # Inicializar review_data_list con todos los checkboxes con un valor de 'off'
    review_data_list = [
        {"id": key, "message": field_to_message.get(key, ""), "value": "off"}
        for key in field_to_message.keys()
    ]

    # Actualizar los valores de los checkboxes que están marcados
    for item in review_data_list:
        if item["id"] in review_data:
            item["value"] = review_data[item["id"]]

    request.review_data = review_data_list
    request.is_reviewed = True
    request.save()

    return redirect("/requests/?reviewDone")


@csrf_exempt
@login_required
def update_request(request, request_id):
    # Get the request object
    curr_request = get_request_by_id(request_id)

    # Update the status and is_reviewed fields
    with transaction.atomic():
        curr_request.status = "EN REVISIÓN"
        curr_request.is_reviewed = False
        print(request.POST.dict())

        # Update the request with the data from the method's request
        for key, value in request.POST.items():
            if hasattr(curr_request, key):
                setattr(curr_request, key, value)

        if isinstance(curr_request, TravelAdvanceRequest):
            expenses = {
                "airportTransport": request.POST.get("airportTransport"),
                "localTransport": request.POST.get("localTransport"),
                "food": request.POST.get("food"),
                "accommodation": request.POST.get("accommodation"),
                "exitTaxes": request.POST.get("exitTaxes"),
                "others": request.POST.get("others"),
                "total": request.POST.get("total"),
            }
            curr_request.expenses = json.dumps(expenses)

        elif isinstance(curr_request, AdvanceLegalization):
            curr_request.total = request.POST.get("total")
            curr_request.advance_total = request.POST.get("advanceTotal")
            curr_request.employee_balance_value = request.POST.get(
                "employeeBalanceValue"
            )
            curr_request.icesi_balance_value = request.POST.get("icesiBalanceValue")

            expensesTable = AdvanceLegalization_Table.objects.filter(
                general_data_id=request_id
            )

            for key, value in request.POST.items():
                match = re.match(r"(\w+)_(\d+)", key)
                if match:
                    field_name, row_number = match.groups()
                    row_number = int(row_number)
                    if row_number < len(expensesTable):
                        expense = expensesTable[row_number]
                        if hasattr(expense, field_name):
                            setattr(expense, field_name, value)
                            expense.save()

        elif isinstance(curr_request, TravelExpenseLegalization):
            """
            'total1': '15568', 'total2': '2863', 'total3': '13425', 'advanceTotal1': '5562', 'advanceTotal2': '10000', 'advanceTotal3': '324', 'employeeBalance1': '10006', 'employeeBalance2': '0', 'employeeBalance3': '13101', 'icesiBalance1': '0', 'icesiBalance2': '-7137', 'icesiBalance3': '0'
            """
            curr_request.total1 = request.POST.get("total1")
            curr_request.total2 = request.POST.get("total2")
            curr_request.total3 = request.POST.get("total3")
            curr_request.advance_total1 = request.POST.get("advanceTotal1")
            curr_request.advance_total2 = request.POST.get("advanceTotal2")
            curr_request.advance_total3 = request.POST.get("advanceTotal3")
            curr_request.employee_balance1 = request.POST.get("employeeBalance1")
            curr_request.employee_balance2 = request.POST.get("employeeBalance2")
            curr_request.employee_balance3 = request.POST.get("employeeBalance3")
            curr_request.icesi_balance1 = request.POST.get("icesiBalance1")
            curr_request.icesi_balance2 = request.POST.get("icesiBalance2")
            curr_request.icesi_balance3 = request.POST.get("icesiBalance3")

            expensesTable = TravelExpenseLegalization_Table.objects.filter(
                travel_info_id=request_id
            )

            for key, value in request.POST.items():
                match = re.match(r"(\w+)_(\d+)", key)
                if match:
                    field_name, row_number = match.groups()
                    row_number = int(row_number)
                    if row_number < len(expensesTable):
                        expense = expensesTable[row_number]
                        if hasattr(expense, field_name):
                            setattr(expense, field_name, value)
                            expense.save()

        curr_request.save()

    Traceability.objects.create(
        modified_by=request.user,
        prev_state="DEVUELTO",
        new_state="EN REVISIÓN",
        reason="Corrección de formulario.",
        date=datetime.now(),
        request=request_id,
    )

    return JsonResponse(
        {
            "message": f"El estado de la solicitud {id} ha sido actualizado correctamente."
        }
    )
