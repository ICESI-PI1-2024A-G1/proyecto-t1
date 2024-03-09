class SearchFilter:
    def __init__(self) -> None:
        filters = [
            "id",
            "document",
            "applicant",
            "manager",
            "initial_date",
            "final_date",
            "past_days",
            "status",
        ]

        # Use this when Request.model is ready
        # filters = vars(Requests())

    def filter(self):
        pass
