from django.urls import path
from . import views

app_name = "forms"

urlpatterns = [
    path("", views.show_forms, name="show_forms"),
    path("form-preview/", views.form_preview, name="form-preview"),
]
