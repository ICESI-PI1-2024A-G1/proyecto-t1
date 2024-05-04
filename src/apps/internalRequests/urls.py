"""
Internal Request urls

This module defines URL patterns for the internal requests application.
"""

from django.urls import path

from apps.internalRequests import views

app_name = "internalRequests"

urlpatterns = [
    path("", views.show_requests, name="show_requests"),
    path("<int:id>/<str:pdf>", views.detail_request, name="show_pdf"),
    path("change-status/<int:id>", views.change_status, name="change_status"),
    path(
        "assign-request/<int:request_id>", views.assign_request, name="assign_request"
    ),
    path("<int:id>/", views.detail_request, name="request_detail"),
    path(
        "show-traceability/<int:request_id>",
        views.show_traceability,
        name="show_traceability",
    ),
    path(
        "update-request/<int:request_id>", views.update_request, name="update_request"
    ),
    # Review paths
    path(
        "travel_advance_request_review",
        views.travel_advance_request,
        name="travel_advance_request",
    ),
    path(
        "travel_expense_legalization_review",
        views.travel_expense_legalization,
        name="travel_expense_legalization",
    ),
    path(
        "advance_legalization_review",
        views.advance_legalization,
        name="advance_legalization",
    ),
    path("billing_account_review", views.billing_account, name="billing_account"),
    path("requisition_review", views.requisition, name="requisition"),
]
