from django.urls import path
from . import views

app_name = "forms"

urlpatterns = [
    path("", views.show_forms, name="show_forms"),
    path("<int:id>/", views.form_details, name="form_details"),
    path("add-form/", views.add_form, name="add_form"),
    path("form-preview/", views.form_preview, name="form-preview"),
    path("load-template/", views.load_excel_template, name="load_template"),
    path("fill-form/<int:id>/", views.fill_form, name="fill_form"),
    path("delete-form/<int:id>/", views.delete_form, name="delete_form"),
]
