from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from apps.forms.models import TravelRequest, TravelInfo, ExpenseDetail
from django.contrib import messages

@csrf_exempt
def travel_advance_request(request):
    today = date.today().isoformat()
    if request.method == "GET":
        return render(request, "travel_advance_request.html", {"today": today})
    else:
        form_data = request.POST

        if form_data.get('signatureStatus') != 'Yes':
            messages.error(request, 'Por favor, firme el formulario.')
            return render(request, "travel_advance_request.html", {"today": today, "form_data": form_data})
        else:
            # Create a new TravelRequest instance
            travel_request = TravelRequest()

            # Set the fields from the form data
            travel_request.request_date = form_data['requestDate']
            travel_request.traveler_name = form_data['travelerName']
            travel_request.id_number = form_data['idNumber']
            travel_request.dependence = form_data['dependence']
            travel_request.cost_center = form_data['costCenter']
            travel_request.destination_city = form_data['destinationCity']
            travel_request.departure_date = form_data['departureDate']
            travel_request.return_date = form_data['returnDate']
            travel_request.travel_reason = form_data['travelReason']
            travel_request.currency = form_data['currency']

            # Serialize the expenses and store them in the expenses field
            expenses = {
                'airportTransport': form_data['airportTransport'],
                'localTransport': form_data['localTransport'],
                'food': form_data['food'],
                'accommodation': form_data['accommodation'],
                'exitTaxes': form_data['exitTaxes'],
                'others': form_data['others'],
                'total': form_data['total'],
            }
            travel_request.set_expenses(expenses)

            travel_request.signature_status = form_data['signatureStatus']
            travel_request.bank = form_data['bank']
            travel_request.account_type = form_data['accountType']
            travel_request.account_number = form_data['accountNumber']
            travel_request.observations = form_data['observations']

            # Save the TravelRequest instance to the database
            travel_request.save()

            messages.success(request, 'Formulario enviado correctamente. Puede revisarlo en la sección de "Solicitudes".')
            return render(request, "travel_advance_request.html", {"form_data": form_data})

@csrf_exempt
def travel_expense_legalization(request):
    if request.method == "GET":
        today = date.today().isoformat()
        return render(request, "travel_expense_legalization.html", {"today": today})
    else:
        form_data = request.POST

        if form_data.get('signatureStatus') != 'Yes':
            messages.error(request, 'Por favor, firme el formulario.')
            return render(request, "travel_expense_legalization.html", {"today": today, "form_data": form_data})
        else:
            travel_legalization = TravelInfo()

            travel_legalization.request_date = form_data['requestDate']
            travel_legalization.traveler_name = form_data['travelerName']
            travel_legalization.id_number = form_data['idNumber']
            travel_legalization.dependence = form_data['dependence']
            travel_legalization.cost_center = form_data['costCenter']
            travel_legalization.destination_city = form_data['destinationCity']
            travel_legalization.departure_date = form_data['departureDate']
            travel_legalization.return_date = form_data['returnDate']
            travel_legalization.travel_reason = form_data['travelReason']
            travel_legalization.total1 = form_data['total1']
            travel_legalization.total2 = form_data['total2']
            travel_legalization.total3 = form_data['total3']
            travel_legalization.advance_total1 = form_data['advanceTotal1']
            travel_legalization.advance_total2 = form_data['advanceTotal2']
            travel_legalization.advance_total3 = form_data['advanceTotal3']
            travel_legalization.employee_balance1 = form_data['employeeBalance1']
            travel_legalization.employee_balance2 = form_data['employeeBalance2']
            travel_legalization.employee_balance3 = form_data['employeeBalance3']
            travel_legalization.icesi_balance1 = form_data['icesiBalance1']
            travel_legalization.icesi_balance2 = form_data['icesiBalance2']
            travel_legalization.icesi_balance3 = form_data['icesiBalance3']
            travel_legalization.signature_status = form_data['signatureStatus'] == 'Yes'
            travel_legalization.bank = form_data['bank']
            travel_legalization.account_type = form_data['accountType']
            travel_legalization.account_number = form_data['accountNumber']
            travel_legalization.observations = form_data['observations']
            travel_legalization.save()

            for i in range(4):
                expense_detail = ExpenseDetail()
                expense_detail.travel_info = travel_legalization
                expense_detail.category = form_data['category_' + str(i)]
                expense_detail.provider = form_data['provider_' + str(i)]
                expense_detail.nit = form_data['nit_' + str(i)]
                expense_detail.concept = form_data['concept_' + str(i)]
                expense_detail.pesos = form_data['pesos_' + str(i)]
                expense_detail.dollars = form_data['dollars_' + str(i)]
                expense_detail.euros = form_data['euros_' + str(i)]
                expense_detail.save()

            messages.success(request, 'Formulario enviado correctamente. Puede revisarlo en la sección de "Solicitudes".')
            return render(request, "travel_expense_legalization.html", {"form_data": form_data})


@csrf_exempt
def advance_legalization(request):
    if request.method == "GET":
        today = date.today().isoformat()
        return render(request, "advance_legalization.html", {"today": today})

@csrf_exempt
def billing_account(request):
    if request.method == "GET":
        today = date.today().isoformat()
        return render(request, "billing_account.html", {"today": today, 'include_cex': True})

@csrf_exempt
def requisition(request):
    if request.method == "GET":
        today = date.today().isoformat()
        return render(request, "requisition.html", {"today": today})

