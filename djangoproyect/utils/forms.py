# forms.py
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm

class CustomUserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        fields = '__all__'  # O selecciona los campos que deseas mostrar