from django.http import JsonResponse
from django.db.models import Q
from applications.requests.models import Requests


class SearchFilter:
    def __init__(self):
        self.filter_mapping = {
            "id": "number",
            "document": "string",
            "applicant": "string",
            "manager": "string",
            "status": "string",
        }

    def is_number(self, query):
        try:
            int(query)
        except ValueError:
            return False

        return True

    def filter_request(self, query):
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

        results = Requests.objects.filter(filters)
        data = [
            {
                "id": result.id,
                "document": result.document,
                "applicant": result.applicant,
                "manager": result.manager,
                "initial_date": result.initial_date,
                "final_date": result.final_date,
                "past_days": result.past_days,
                "status": result.status,
            }
            for result in results
        ]
        return JsonResponse(data, safe=False)
