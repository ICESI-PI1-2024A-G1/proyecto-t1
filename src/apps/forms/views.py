from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import date

@csrf_exempt
def travel_advance_request(request):
    if request.method == "GET":
        today = date.today().isoformat()
        return render(request, "travel_advance_request.html", {"today": today})

@csrf_exempt
def travel_expense_legalization(request):
    if request.method == "GET":
        today = date.today().isoformat()
        return render(request, "travel_expense_legalization.html", {"today": today})

@csrf_exempt
def advance_legalization(request):
    if request.method == "GET":
        return render(request, "advance_legalization.html")

@csrf_exempt
def billing_account(request):
    if request.method == "GET":
        return render(request, "billing_account.html")

@csrf_exempt
def requisition(request):
    if request.method == "GET":
        return render(request, "requisition.html")

