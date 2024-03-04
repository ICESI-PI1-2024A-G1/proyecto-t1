from django.urls import path

from applications.requests import views


urlpatterns = [
    path("change-request/<int:id>", views.change_requests),
    path("", views.show_requests),
]
