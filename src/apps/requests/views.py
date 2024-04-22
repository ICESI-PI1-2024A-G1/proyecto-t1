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

def search(request, query):
    """
    Performs a search for requests based on a query string.

    HTTP Method:
    - GET

    Dependencies:
    - sharepoint_api: For searching request data based on the query.

    Parameters:
    - request: Django request object.
    - query: Query string for searching requests.

    Returns:
    - JsonResponse: JSON response containing search results or error message.
    """
    try:
        results = sharepoint_api.search_data(query=query)

        if results.status_code == 200:
            return JsonResponse(json.loads(results.content), safe=False)
        else:
            raise Http404("El archivo Excel no está disponible")
    except Http404 as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        return JsonResponse(
            {"error": f"No se pudo realizar la operación: {str(e)}"}, status=500
        )


@never_cache
@login_required
def show_requests(request):
    """
    Renders a page displaying all requests.

    HTTP Method:
    - GET

    Dependencies:
    - sharepoint_api: For retrieving all request data.
    - Team: Model for accessing team information.

    Parameters:
    - request: Django request object.

    Returns:
    - render: Renders the HTML template with request data.
    """
    try:
        response = sharepoint_api.get_all_requests()
        if response.status_code == 200:
            requests_data = json.loads(response.content)
            user_str = request.user.__str__()
            if not request.user.is_superuser:
                requests_data = [ r for r in requests_data if r["manager"] == user_str ]
            for r in requests_data:
                r["team"] = "" if math.isnan(r["team"]) else int(r["team"])
                r["status_color"] = status_colors[r["status"]]

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
    Renders a page displaying details of a specific request.

    HTTP Method:
    - GET

    Dependencies:
    - sharepoint_api: For retrieving details of the specified request.

    Parameters:
    - request: Django request object.
    - id: ID of the request to be displayed.

    Returns:
    - render: Renders the HTML template with request details.
    """
    try:
        api_response = sharepoint_api.get_request_by_id(id)
        detail = json.loads(api_response.content)
        if api_response.status_code == 200:
            return render(
                request,
                "request-detail.html",
                {"request": detail},
            )
        else:
            raise Http404(f"No se encontró la solicitud con ID {id} en SharePointAPI.")
    except Http404 as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        return JsonResponse(
            {"error": f"No se pudo realizar la operación: {str(e)}"}, status=500
        )
