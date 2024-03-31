"""
Request urls

This module defines URL patterns for the login application.
"""

from django.urls import path
from . import views

app_name = "login"

urlpatterns = [
    path("", views.login_view, name="login_view"),
    path("logout/", views.login_view, name="login_view"),
    path("resetPassword/", views.reset_password_view, name="reset_password_view"),
    path(
        "resetPassword/verifyIdentity/",
        views.verify_email_reset_view,
        name="verify_email_reset_view",
    ),
    path("changePassword/", views.change_password_view, name="change_password_view"),
    path("verifyEmail/", views.verify_email_view, name="verifyEmail_view"),
]
