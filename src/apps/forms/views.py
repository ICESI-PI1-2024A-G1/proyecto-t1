from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.db import transaction
from datetime import date
from apps.forms.models import *
from django.contrib import messages
from django.db.models import Prefetch
import json


# Calculate the next ID for the forms
def get_next_id():
    max_id1 = TravelAdvanceRequest.objects.all().aggregate(Max("id"))["id__max"] or 0
    max_id2 = AdvanceLegalization.objects.all().aggregate(Max("id"))["id__max"] or 0
    max_id3 = BillingAccount.objects.all().aggregate(Max("id"))["id__max"] or 0
    max_id4 = Requisition.objects.all().aggregate(Max("id"))["id__max"] or 0
    max_id5 = (
        TravelExpenseLegalization.objects.all().aggregate(Max("id"))["id__max"] or 0
    )
    return max(max_id1, max_id2, max_id3, max_id4, max_id5) + 1


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
    today = date.today().isoformat()
    cities_data = get_cities_with_countries()
    bank_data = get_bank_data()
    account_types = get_account_types()
    dependences = get_dependence_data()
    cost_centers = get_cost_center_data()

    context = {
        "today": today,
        "cities": cities_data,
        "banks": bank_data,
        "account_types": account_types,
        "dependences": dependences,
        "cost_centers": cost_centers,
    }

    return context


@login_required
@csrf_exempt
def travel_advance_request(request):
    context = create_context()

    if request.method == "GET":
        return render(request, "userForms/travel_advance_request.html", context)
    else:
        form_data = request.POST
        context["form_data"] = form_data

        if form_data.get("signatureStatus") != "Yes":
            messages.error(request, "Por favor, firme el formulario.")
            return render(
                request,
                "userForms/travel_advance_request.html",
                context,
            )
        elif form_data.get("departureDate") > form_data.get("returnDate"):
            messages.error(
                request,
                "La fecha de regreso no puede ser anterior a la fecha de salida.",
            )
            return render(
                request,
                "userForms/travel_advance_request.html",
                context,
            )

        else:
            # Create a new TravelRequest instance
            travel_request = TravelAdvanceRequest()

            # Set the fields from the form data
            travel_request.request_date = form_data["requestDate"]
            travel_request.fullname = form_data["fullName"]
            travel_request.id_person = form_data["idNumber"]
            travel_request.dependence = form_data["dependence"]
            travel_request.cost_center = form_data["costCenter"]
            travel_request.destination_city = form_data["destinationCity"]
            travel_request.departure_date = form_data["departureDate"]
            travel_request.return_date = form_data["returnDate"]
            travel_request.travel_reason = form_data["travelReason"]
            travel_request.currency = form_data["currency"]

            # Serialize the expenses and store them in the expenses field
            expenses = {
                "airportTransport": form_data["airportTransport"],
                "localTransport": form_data["localTransport"],
                "food": form_data["food"],
                "accommodation": form_data["accommodation"],
                "exitTaxes": form_data["exitTaxes"],
                "others": form_data["others"],
                "total": form_data["total"],
            }
            travel_request.set_expenses(expenses)

            travel_request.signature_status = form_data["signatureStatus"]
            travel_request.bank = form_data["bank"]
            travel_request.account_type = form_data["accountType"]
            travel_request.account_number = form_data["accountNumber"]
            travel_request.observations = form_data["observations"]
            travel_request.signatureInput = form_data["signatureInput"]

            # Set the id to the next available id
            with transaction.atomic():
                travel_request.id = get_next_id()

            # Save the TravelRequest instance to the database
            travel_request.save()

            messages.success(
                request,
                "Formulario enviado correctamente. Puede revisarlo en la sección de Solicitudes.",
            )
            context["form_data"] = None
            return render(
                request, "userForms/travel_advance_request.html", {"today": date.today().isoformat()}
            )


@login_required
@csrf_exempt
def travel_expense_legalization(request):
    context = create_context()

    if request.method == "GET":
        return render(
            request,
            "userForms/travel_expense_legalization.html",
            context,
        )
    else:
        form_data = request.POST
        context["form_data"] = form_data

        if form_data.get("signatureStatus") != "Yes":
            messages.error(request, "Por favor, firme el formulario.")
            return render(
                request,
                "userForms/travel_expense_legalization.html",
                context,
            )
        elif form_data.get("departureDate") > form_data.get("returnDate"):
            messages.error(
                request,
                "La fecha de regreso no puede ser anterior a la fecha de salida.",
            )
            return render(
                request,
                "userForms/travel_expense_legalization.html",
                context,
            )
        else:
            # Create a new GeneralData object
            travel_legalization = TravelExpenseLegalization()

            # Set the fields of the GeneralData object
            travel_legalization.request_date = form_data["requestDate"]
            travel_legalization.fullname = form_data["fullName"]
            travel_legalization.id_person = form_data["idNumber"]
            travel_legalization.dependence = form_data["dependence"]
            travel_legalization.cost_center = form_data["costCenter"]
            travel_legalization.destination_city = form_data["destinationCity"]
            travel_legalization.departure_date = form_data["departureDate"]
            travel_legalization.return_date = form_data["returnDate"]
            travel_legalization.travel_reason = form_data["travelReason"]
            travel_legalization.total1 = form_data["total1"]
            travel_legalization.total2 = form_data["total2"]
            travel_legalization.total3 = form_data["total3"]
            travel_legalization.advance_total1 = form_data["advanceTotal1"]
            travel_legalization.advance_total2 = form_data["advanceTotal2"]
            travel_legalization.advance_total3 = form_data["advanceTotal3"]
            travel_legalization.employee_balance1 = form_data["employeeBalance1"]
            travel_legalization.employee_balance2 = form_data["employeeBalance2"]
            travel_legalization.employee_balance3 = form_data["employeeBalance3"]
            travel_legalization.icesi_balance1 = form_data["icesiBalance1"]
            travel_legalization.icesi_balance2 = form_data["icesiBalance2"]
            travel_legalization.icesi_balance3 = form_data["icesiBalance3"]
            travel_legalization.signature_status = form_data["signatureStatus"] == "Yes"
            travel_legalization.bank = form_data["bank"]
            travel_legalization.account_type = form_data["accountType"]
            travel_legalization.account_number = form_data["accountNumber"]
            travel_legalization.observations = form_data["observations"]
            travel_legalization.signatureInput = form_data["signatureInput"]

            # Set the id to the next available id
            with transaction.atomic():
                travel_legalization.id = get_next_id()

            # Save the GeneralData object
            travel_legalization.save()

            i = 0
            while f"category_{i}" in form_data:
                # Create a new ExpenseDetail object
                expense_detail = TravelExpenseLegalization_Table()

                expense_detail.travel_info = travel_legalization
                expense_detail.category = form_data["category_" + str(i)]
                expense_detail.provider = form_data["provider_" + str(i)]
                expense_detail.nit = form_data["nit_" + str(i)]
                expense_detail.concept = form_data["concept_" + str(i)]
                expense_detail.pesos = form_data["pesos_" + str(i)]
                expense_detail.dollars = form_data["dollars_" + str(i)]
                expense_detail.euros = form_data["euros_" + str(i)]
                expense_detail.save()

                i += 1

            messages.success(
                request,
                "Formulario enviado correctamente. Puede revisarlo en la sección de Solicitudes.",
            )
            context["form_data"] = None
            return render(
                request, "userForms/travel_expense_legalization.html", context
            )


@login_required
@csrf_exempt
def advance_legalization(request):
    context = create_context()

    if request.method == "GET":
        return render(request, "userForms/advance_legalization.html", context)
    else:
        form_data = request.POST
        context["form_data"] = form_data

        if form_data.get("signatureStatus") != "Yes":
            messages.error(request, "Por favor, firme el formulario.")
            return render(
                request,
                "userForms/advance_legalization.html",
                context,
            )
        else:
            # Create a new GeneralData object
            advance_legalization = AdvanceLegalization()

            # Set the fields of the GeneralData object
            advance_legalization.request_date = form_data["requestDate"]
            advance_legalization.fullname = form_data["fullName"]
            advance_legalization.id_person = form_data["idNumber"]
            advance_legalization.dependence = form_data["dependence"]
            advance_legalization.cost_center = form_data["costCenter"]
            advance_legalization.purchase_reason = form_data["purchaseReason"]
            advance_legalization.total = form_data["total"]
            advance_legalization.advance_total = form_data["advanceTotal"]
            advance_legalization.employee_balance_value = form_data[
                "employeeBalanceValue"
            ]
            advance_legalization.icesi_balance_value = form_data["icesiBalanceValue"]
            advance_legalization.signature_status = (
                form_data["signatureStatus"] == "Yes"
            )
            advance_legalization.bank = form_data["bank"]
            advance_legalization.account_type = form_data["accountType"]
            advance_legalization.account_number = form_data["accountNumber"]
            advance_legalization.observations = form_data["observations"]
            advance_legalization.signatureInput = form_data["signatureInput"]

            # Set the id to the next available id
            with transaction.atomic():
                advance_legalization.id = get_next_id()

            # Save the GeneralData object
            advance_legalization.save()

            # Loop through the expense details
            i = 0
            while f"category_{i}" in form_data:
                # Create a new ExpenseDetail object
                expense_detail = AdvanceLegalization_Table()

                # Set the fields of the ExpenseDetail object
                expense_detail.general_data = advance_legalization
                expense_detail.category = form_data[f"category_{i}"]
                expense_detail.provider = form_data[f"provider_{i}"]
                expense_detail.pesos = form_data[f"pesos_{i}"]
                expense_detail.concept = form_data[f"concept_{i}"]

                # Save the ExpenseDetail object
                expense_detail.save()

                i += 1

            messages.success(
                request,
                "Formulario enviado correctamente. Puede revisarlo en la sección de Solicitudes.",
            )
            context["form_data"] = None
            return render(
                request, "userForms/advance_legalization.html", context
            )


@login_required
@csrf_exempt
def billing_account(request):
    context = create_context()
    context["include_cex"] = True

    if request.method == "GET":
        return render(
            request,
            "userForms/billing_account.html",
            context,
        )
    else:
        form_data = request.POST
        context["form_data"] = form_data

        if form_data.get("signatureStatus") != "Yes":
            context["form_data"] = form_data
            messages.error(request, "Por favor, firme el formulario.")
            return render(
                request,
                "userForms/billing_account.html",
                context,
            )
        else:
            # Create a new GeneralData object
            billing_account = BillingAccount()

            # Set the fields of the GeneralData object
            billing_account.request_date = form_data["requestDate"]
            billing_account.fullname = form_data["fullName"]
            billing_account.id_person = form_data["idNumber"]
            billing_account.value = form_data["value"]
            billing_account.concept_reason = form_data["conceptReason"]
            billing_account.retention = form_data["retention"]
            billing_account.tax_payer = form_data["taxPayer"]
            billing_account.resident = form_data["resident"]
            billing_account.request_city = form_data["requestCity"]
            billing_account.address = form_data["address"]
            billing_account.phone_number = form_data["phoneNumber"]
            billing_account.signature_status = form_data["signatureStatus"] == "Yes"
            billing_account.bank = form_data["bank"]
            billing_account.account_type = form_data["accountType"]
            billing_account.account_number = form_data["accountNumber"]
            billing_account.cex_number = form_data["cexNumber"]
            billing_account.signatureInput = form_data["signatureInput"]

            # Set the id to the next available id
            with transaction.atomic():
                billing_account.id = get_next_id()

            # Save the GeneralData object
            billing_account.save()

            messages.success(
                request,
                "Formulario enviado correctamente. Puede revisarlo en la sección de Solicitudes.",
            )
            context["form_data"] = None
            return render(
                request,
                "userForms/billing_account.html",
                context,
            )


@login_required
@csrf_exempt
def requisition(request):
    context = create_context()

    if request.method == "GET":
        return render(request, "userForms/requisition.html", context)
    else:
        form_data = request.POST
        context["form_data"] = form_data

        if form_data.get("signatureStatus") != "Yes":
            messages.error(request, "Por favor, firme el formulario.")
            return render(
                request,
                "userForms/requisition.html",
                context,
            )
        else:
            # Create a new GeneralData object
            requisition = Requisition()

            # Set the fields of the GeneralData object
            requisition.request_date = form_data["requestDate"]
            requisition.fullname = form_data["fullName"]
            requisition.id_person = form_data["idNumber"]
            requisition.work = form_data["work"]
            requisition.dependence = form_data["dependence"]
            requisition.cenco = form_data["cenco"]
            requisition.id_value = form_data["idValue"]
            requisition.description = form_data["description"]
            requisition.signature_status = form_data["signatureStatus"] == "Yes"
            requisition.bank = form_data["bank"]
            requisition.account_type = form_data["accountType"]
            requisition.account_number = form_data["accountNumber"]
            requisition.observations = form_data["observations"]
            requisition.signatureInput = form_data["signatureInput"]

            # Set the id to the next available id
            with transaction.atomic():
                requisition.id = get_next_id()

            # Save the GeneralData object
            requisition.save()

            messages.success(
                request,
                "Formulario enviado correctamente. Puede revisarlo en la sección de Solicitudes.",
            )
            context["form_data"] = None
            return render(request, "userForms/requisition.html", context)
