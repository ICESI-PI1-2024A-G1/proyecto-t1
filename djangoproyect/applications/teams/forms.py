from django import forms
from django.contrib.auth import get_user_model
from .models import Team

User = get_user_model()


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
        labels = {
            "name": "Nombre",
            "description": "Descripción",
            "leader": "Líder",
            "members": "Miembros (al menos 1)",
        }

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        leaders_without_team = User.objects.filter(leading_team__isnull=True)
        self.fields["leader"].queryset = leaders_without_team

        instance = kwargs.get("instance")
        if instance:
            leader_id = instance.leader.id
            self.fields["members"].queryset = User.objects.exclude(id=leader_id)

    def clean_members(self):
        members = self.cleaned_data.get("members")
        leader = self.cleaned_data.get("leader")

        if leader and leader in members:
            raise forms.ValidationError(
                "El líder no puede ser un miembro de su equipo."
            )

        return members
