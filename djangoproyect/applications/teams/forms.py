from django import forms
from django.contrib.auth.models import User
from .models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "description", "leader", "members"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "leader": forms.Select(attrs={"class": "form-control"}),
            "members": forms.CheckboxSelectMultiple(),
        }
