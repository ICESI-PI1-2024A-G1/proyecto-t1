from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import date

@csrf_exempt
def travel_advance_request(request):
    today = date.today().isoformat()
    if request.method == "GET":
        return render(request, "travel_advance_request.html", {"today": today})
    else:
        form_data = request.POST.dict()
        print(form_data)
        if form_data.get('signatureStatus') != 'Yes':
            return render(request, "travel_advance_request.html", {"message": "Por favor, firme el formulario.", "today": today, "form_data": form_data})
        else:
            return render(request, "travel_advance_request.html", {"message": "Formulario enviado correctamente. Puede revisarlo en la sección de 'Solicitudes'.", "form_data": form_data})

@csrf_exempt
def travel_expense_legalization(request):
    if request.method == "GET":
        today = date.today().isoformat()
        return render(request, "travel_expense_legalization.html", {"today": today})

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

