from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Case, When, Value, IntegerField
from applications.permissions.model.filter_logic import SearchFilter
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
import json


User = get_user_model()


@login_required
def permissions_view(request):
    users = User.objects.annotate(
        is_superuser_order=Case(
            When(is_superuser=True, then=Value(1)),
            default=Value(2),
            output_field=IntegerField(),
        )
    ).order_by('is_superuser_order', 'last_name')
    return render(request, "permissions.html", {"users": users})

def search(request, query):
    # print(query)
    users_filter = SearchFilter()

    return users_filter.filter_users(query)


@csrf_exempt
def update_user_permissions(request):
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