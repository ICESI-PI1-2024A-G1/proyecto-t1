from django.urls import path

from applications.requests import views


urlpatterns = [
    path("change-requests/", views.change_requests),
    path("/", views.show_requests),
]
