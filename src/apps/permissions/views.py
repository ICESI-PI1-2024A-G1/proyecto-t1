"""
Permissions' views modules

This module contains view functions for managing permissions for users in the appliactions
it is intended for the admin to manage how the users can access the data in the application
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Case, When, Value, IntegerField
from apps.permissions.model.filter_logic import SearchFilter
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
import json


User = get_user_model()


@never_cache
@login_required
def permissions_view(request):
    """
    View function for displaying permissions.

    Only accessible to superusers, redirects if the user is not a superuser.
    Retrieves users and orders them by superuser status and last name.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered permissions.html template with users.
    """
    if not request.user.is_superuser:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    users = User.objects.annotate(
        is_superuser_order=Case(
            When(is_superuser=True, then=Value(1)),
            default=Value(2),
            output_field=IntegerField(),
        )
    ).order_by('is_superuser_order', 'last_name')
    return render(request, "permissions.html", {"users": users})

def search(request, query):
    """
    View function for searching users.

    This function is responsible for handling user search queries.
    
    Args:
        request (HttpRequest): The request object.
        query (str): The search query.

    Returns:
        JsonResponse: JSON response containing filtered users.

    Notes:
        The function initializes a SearchFilter object and uses it to filter users based on the provided query.
    """
    users_filter = SearchFilter()

    return users_filter.filter_users(query)


@csrf_exempt
def update_user_permissions(request):
    """
    View function for updating user permissions.

    This function handles the updating of user permissions'.
    It expects a POST request containing JSON data with user IDs and permission changes.
    It updates the permissions for the specified users.

    Args:
        request (HttpRequest): The request object.

    Returns:
        JsonResponse: JSON response indicating success or failure.

    Notes:
        - The function is exempted from CSRF protection.
        - Expects a POST request with JSON data containing user IDs and their permission changes.
        - Iterates over the received data, updates user permissions accordingly, and saves the changes.
        - Returns a JSON response indicating the status of the operation.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        for item in data:
            user = User.objects.get(id=item['id'])
            if 'is_staff' in item:
                user.is_staff = item['is_staff']
            if 'is_leader' in item:
                user.is_leader = item['is_leader']
            user.save()
        return JsonResponse({'status': 'success', 'message': 'Permisos actualizados correctamente.'})
    else:
        return JsonResponse({'status': 'failed', 'message': 'Los permisos no se pudieron actualizar.'})