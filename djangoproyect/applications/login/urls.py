from django.urls import path

from applications.login import views


urlpatterns = [
    path("", views.login_view),
]
