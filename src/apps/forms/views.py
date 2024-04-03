import math
from django.shortcuts import redirect, render

# Create your views here.

from django.conf import settings
from api.sharepoint_api import SharePointAPI
import os
from django.views.decorators.csrf import csrf_exempt
import json

from apps.forms.models import ExcelForm, FormField


@csrf_exempt
def show_forms(request):
    if request.method == "GET":
        forms = ExcelForm.objects.all()
        return render(request, "show-forms.html", {"forms":forms})


@csrf_exempt
def add_form(request):
    if request.method == "GET":
        return render(request, "add-form.html")
    elif request.method == "POST":
        nombre = request.POST.get("name")
        descripcion = request.POST.get("description")
        excel_template = request.FILES.get("excel_template")
        form_fields_data = json.loads(request.POST.get("form_fields", "[]"))
        print(excel_template)
        # Crear una nueva instancia de ExcelForm
        excel_form = ExcelForm.objects.create(
            name=nombre,
            description=descripcion,
            excel_file=excel_template,
        )

        print(form_fields_data)
        # Procesar los datos de los campos del formulario
        for field_data in form_fields_data:
            field_type = field_data["type"]
            col_idx = field_data["col_idx"]
            row_idx = field_data["row_idx"]
            form_field = FormField.objects.create(
                type=field_type,
                label=field_data["label"],
                name=f"{field_data["type"]}-{row_idx}-{col_idx}",
                col_idx=col_idx,
                row_idx=row_idx,
            )
            excel_form.form_fields.add(form_field)

        # Guardar y redirigir
        excel_form.save()
        return redirect("/forms/")


@csrf_exempt
def load_excel_template(request):
    if request.method == "POST":
        template_file = request.FILES["excel_template"]
        sharepoint_api = SharePointAPI(settings.EXCEL_FILE_PATH)
        api_response = sharepoint_api.get_form_render(excel_file=template_file)
        sheet = json.loads(api_response.content)
        return render(request, "excel-preview.html", {"sheet": sheet})

def form_details(request, id):
    if request.method == "GET":
        form = ExcelForm.objects.get(pk=id)
        return render(request, "dynamic-form.html", {"form":form, "isPreview":False, "showBackBtn": True})

@csrf_exempt
def form_preview(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        form_fields = data.get("form_fields")
        # print(form_fields)
        form = {
            "form_fields": {
                "all": form_fields
            }
        }
        return render(
            request, "dynamic-form.html", {"form": form, "isPreview": True, "showBackBtn": False}
        )

@csrf_exempt
def fill_form(request, id):
    if request.method == "POST":
        post_request = request.POST
        form_fields = []
        for key, value in post_request.items():
            [ field_type, row_idx, col_idx ] = key.split("-")
            form_fields.append({
                "type": field_type,
                "row_idx": row_idx,
                "col_idx": col_idx,
                "value": value,
            })
        
        excel_form = ExcelForm.objects.get(pk=id)
        sharepoint_api = SharePointAPI(settings.EXCEL_FILE_PATH)
        sharepoint_api.fill_form(excel_form.excel_file, form_fields)
        return redirect("/forms/")
