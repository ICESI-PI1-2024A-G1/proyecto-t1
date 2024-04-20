from django.urls import path
from . import views

app_name = "forms"

urlpatterns = [
    path("travel_advance_request", views.travel_advance_request, name="travel_advance_request"),
    path("travel_expense_legalization", views.travel_expense_legalization, name="travel_expense_legalization"),
    path("advance_legalization", views.advance_legalization, name="advance_legalization"),
    path("billing_account", views.billing_account, name="billing_account"),
    path("requisition", views.requisition, name="requisition"),
]
