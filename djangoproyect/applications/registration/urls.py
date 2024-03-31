"""
Registration urls

This module defines URL patterns for the registration application.
"""

from django.urls import path
from . import views

app_name = "registration"

urlpatterns = [
    path("", views.register_view, name="register_view"),
    path("verifyEmail/", views.verify_email_view, name="verifyEmail_view"),
]
