"""
Urls module

This module contains URL configuration for the Permissions application in Django.
"""
from django.urls import path
from . import views

app_name = 'permissions'

urlpatterns = [
    path("", views.permissions_view, name='permissions_view'),
    path("search/<str:query>", views.search, name="search"),
    path('update_user_permissions/', views.update_user_permissions, name='update_user_permissions'),
]