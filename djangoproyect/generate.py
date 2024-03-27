import requests


class SearchFilter:
    def __init__(self, api):
        self.api = api
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

        filters = {}
        for field, value in query_dict.items():
            if field in self.filter_mapping and value != "None":
                if self.filter_mapping[field] == "number" and self.is_number(value):
                    filters[field] = int(value)
                elif self.filter_mapping[field] == "string":
                    filters[field] = value

        if not filters:
            return []

        response = requests.get(self.api, params=filters)
        if response.status_code == 200:
            return response.json()
        else:
            return []
