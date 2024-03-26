from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Case, When, Value, IntegerField
from applications.permissions.model.filter_logic import SearchFilter


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