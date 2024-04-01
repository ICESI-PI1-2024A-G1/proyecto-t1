from django.shortcuts import render

# Create your views here.


def show_forms(request):
    return render(request, "show-forms.html")
