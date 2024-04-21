"""
Internal Request urls

This module defines URL patterns for the internal requests application.
"""
from django.urls import path

from apps.internalRequests import views

app_name = "internalRequests"

urlpatterns = [
    path("", views.show_requests, name="show_requests"),
    path("change-status/<int:id>", views.change_status, name="change_status"),
]
