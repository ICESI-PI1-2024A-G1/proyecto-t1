"""
Request urls

This module defines URL patterns for the requests application.
"""
from django.urls import path

from apps.requests import views

app_name = "requests"

urlpatterns = [
    path("", views.show_requests, name="show_requests"),
    path("change-status/<int:id>", views.change_status, name="change_status"),
    path("search/<str:query>", views.search, name="search"),
    path("<int:id>/", views.detail_request, name="request_detail"),
    path(
        "assign-request/<int:request_id>", views.assign_request, name="assign_request"
    ),
    path(
        "show-traceability/<int:request_id>",
        views.show_traceability,
        name="show_traceability",
    ),
]
