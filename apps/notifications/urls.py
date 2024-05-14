"""
Request urls

This module defines URL patterns for the requests application.
"""

from django.urls import path

from apps.notifications import views

app_name = "notifications"

urlpatterns = [
    path("", views.show_notifications, name="show_notifications"),
]
