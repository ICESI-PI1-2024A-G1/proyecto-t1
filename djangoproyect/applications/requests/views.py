from django.shortcuts import render


# Create your views here.
def change_requests(request):
    return render(request, "change-requests.html")


def show_requests(request):
    context = {
        'requests': [
            { "document": 10, "applicant": "belso", "manager": "marin", "initial_date": "2020/23/22", "past_days": 3, "status": "en proceso"  }
        ]
    }
    return render(request, "show-requests.html")
