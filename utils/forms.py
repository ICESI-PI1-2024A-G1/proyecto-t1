# forms.py
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm


class CustomUserChangeForm(BaseUserChangeForm):
    """
    Custom user change form for editing user details.

    This form inherits from the Django base UserChangeForm.

    Attributes:
        Meta: Meta class defining the form's metadata.
    """

    class Meta(BaseUserChangeForm.Meta):
        """
        Meta class defining the form's metadata.

        Attributes:
            fields (str or list): Specify the fields to include in the form.
                Use '__all__' to include all fields or provide a list of field names.
        """

        fields = "__all__"
