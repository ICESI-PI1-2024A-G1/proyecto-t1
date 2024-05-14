from django.urls import path
from . import views

app_name = "contact"
"""
Application namespace.

This variable defines the namespace for the contact app.
"""

urlpatterns = [
    path("", views.sendEmail_view, name="email_contact"),
]
