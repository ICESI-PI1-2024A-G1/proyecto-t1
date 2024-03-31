from django import forms
from django.contrib.auth import get_user_model
from .models import Team

User = get_user_model()


class TeamForm(forms.ModelForm):
    """
    Form for handling team data input.

    Attributes:
        Meta (inner class): Specifies the model and fields to include in the form.
        widgets (dict): Defines the HTML widget types for form fields.
        labels (dict): Customizes labels for form fields.

    Methods:
        __init__(self, *args, **kwargs): Initializes form with custom logic.
        clean_members(self): Custom validation to ensure leader is not included as a member.

    Note:
        This form is used for creating and updating team data.
    """

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
        """
        Custom validation method to ensure leader is not included as a member.

        Returns:
            queryset: Validated members queryset.

        Raises:
            forms.ValidationError: If the leader is selected as a member.
        """
        members = self.cleaned_data.get("members")
        leader = self.cleaned_data.get("leader")

        if leader and leader in members:
            raise forms.ValidationError(
                "El líder no puede ser un miembro de su equipo."
            )

        return members
