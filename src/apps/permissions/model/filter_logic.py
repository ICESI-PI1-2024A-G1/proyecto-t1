"""
Filter Logic Permissions

This module contains a class for filtering users based on search criteria.
"""
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db.models import Case, When, Value, IntegerField


User = get_user_model()


class SearchFilter:
    """
    Class: SearchFilter

    A utility class for filtering users based on search criteria.

    Attributes:
        filter_mapping (dict): A mapping of field names to their types (e.g., "string" or "number").
    """
    def __init__(self):
        """
        Initializes the SearchFilter class with a mapping of field names to their types.
        """

        self.filter_mapping = {
            "id": "string",
            "last_name": "string",
            "first_name": "string",
            "email": "string",
        }
        
    def is_number(self, query):
        """
        Checks if a given query can be converted to an integer.

        Args:
            query (str): The query string.

        Returns:
            bool: True if the query can be converted to an integer, False otherwise.
        """
        try:
            int(query)
        except ValueError:
            return False

        return True

    def filter_users(self, query):
        """
        Filters users based on the provided search query.

        Args:
            query (str): The search query.

        Returns:
            JsonResponse: JSON response containing filtered user data.

        Notes:
            - Initializes query dictionary based on filter mapping.
            - Constructs filters based on query dictionary and filter mapping.
            - Retrieves users matching the filters and orders them.
            - Constructs JSON response containing user data.
        """
        query_dict = {k: query for k in self.filter_mapping.keys()}
        filters = Q()
        for field, value in query_dict.items():
            if field in self.filter_mapping and value != "None":
                # print("Acutual val: ", value)
                if self.filter_mapping[field] == "number":
                    try:
                        res = int(value)
                        filters |= Q(**{field: res})
                    except ValueError:
                        pass
                else:
                    if value != "None":
                        filters |= Q(**{field: value})
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
        
