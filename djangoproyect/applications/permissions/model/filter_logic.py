from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db.models import Case, When, Value, IntegerField


User = get_user_model()


class SearchFilter:
    def __init__(self):
        self.filter_mapping = {
            "id": "string",
            "last_name": "string",
            "first_name": "string",
            "email": "string",
        }
        
    def is_number(self, query):
        try:
            int(query)
        except ValueError:
            return False

        return True

    def filter_users(self, query):
        query_dict = {k: query for k in self.filter_mapping.keys()}

        # print(query_dict)

        filters = Q()
        for field, value in query_dict.items():
            if field in self.filter_mapping and value != "None":
                # print("Acutual val: ", value)
                if self.filter_mapping[field] == "number":
                    try:
                        res = int(value)
                        filters |= Q(**{field: res})
                        # print(filters)
                    except ValueError:
                        pass
                else:
                    if value != "None":
                        filters |= Q(**{field: value})
                        # print(filters)
        results = User.objects.annotate(
            is_superuser_order=Case(
                When(is_superuser=True, then=Value(1)),
                default=Value(2),
                output_field=IntegerField(),
                )
            ).order_by('is_superuser_order', 'last_name').filter(filters)
        data = [
            {
                "id": result.id,
                "last_name": result.last_name,
                "first_name": result.first_name,
                "email": result.email,
                "is_staff": result.is_staff,
                "is_leader": result.is_leader,
                "is_superuser": result.is_superuser,
            }
            for result in results
        ]
        return JsonResponse(data, safe=False)
        
