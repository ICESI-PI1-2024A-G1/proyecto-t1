"""
Request urls

This module defines URL patterns for the requests application.
"""
from django.urls import path

from apps.requests import views

app_name = "requests"

urlpatterns = [
    path("", views.show_requests, name="show_requests"),
    path("search/<str:query>", views.search, name="search"),
    path("<int:id>/", views.detail_request, name="request_detail"),
]
