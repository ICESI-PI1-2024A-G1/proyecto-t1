"""
Request views

This module contains views for handling requests-related operations within the application.
"""
from datetime import datetime
import json
import math
import os
import traceback
from django.http import Http404, JsonResponse
from django.shortcuts import render
from api.sharepoint_api import SharePointAPI
from apps.requests.models import SharePoint
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib.auth import get_user_model
import utils.utils as utils

from apps.teams.models import Team

from django.conf import settings

sharepoint_api = SharePointAPI(settings.EXCEL_FILE_PATH)

User = get_user_model()

status_colors = {
    "EN PROCESO": "primary",
    "APROBADO - CENCO": "success",
    "RECHAZADO - CENCO": "danger",
    "APROBADO - DECANO": "success",
    "RECHAZADO - DECANO": "danger",
    "PAGADO - CONTABILIDAD": "info",
    "RECHAZADO - CONTABILIDAD": "danger",
    "CERRADO": "secondary",
}

@never_cache
@login_required
def show_requests(request):
    """
    View function to display SharePoint requests.

    This function retrieves SharePoint requests based on the user's permissions and renders them in a template.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: The HTTP response containing the rendered template with SharePoint requests.

    Raises:
        Http404: If the requests cannot be loaded.
    """
    try:
        if request.method == "GET":
            requests_data = SharePoint.objects.all()
            user_str = request.user.__str__()
            if not request.user.is_superuser:
                if request.user.is_leader:
                    requests_data = [r for r in requests_data if r.team == Team.objects.get(leader_id=request.user.id).id]
                elif request.user.is_member:
                    requests_data = [r for r in requests_data if r.manager == user_str]
            for r in requests_data:
                r.team = "" if math.isnan(r.team) else int(r.team)
                r.status_color = status_colors[r.status]

            return render(request, "show-requests.html", {"requests": requests_data})
        else:
            raise Http404("No se pudieron cargar las solicitudes.")
    except Http404 as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        return JsonResponse(
            {"error": f"No se pudo realizar la operación: {str(e)}"}, status=500
        )

@never_cache
@login_required
def detail_request(request, id):
    """
    View function to display details of a SharePoint request.

    This function retrieves details of a SharePoint request by its ID and renders them in a template.

    Args:
        request (HttpRequest): The HTTP request.
        id (int): The ID of the SharePoint request.

    Returns:
        HttpResponse: The HTTP response containing the rendered template with SharePoint request details.

    Raises:
        Http404: If the requested SharePoint request does not exist.
    """
    try:
        if request.method == "GET":
            request_data = SharePoint.objects.get(id=id)
            return render(request, "request-detail.html", {"request": request_data})
        else:
            raise Http404(f"No se encontró la solicitud con ID {id} en SharePointAPI.")
    except Http404 as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        return JsonResponse(
            {"error": f"No se pudo realizar la operación: {str(e)}"}, status=500
        )
