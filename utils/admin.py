""" Django admin module.
This module contains the classes and the add-ons
to the django administrator page it defines which
field would be able to edit, search, add, and display.
Also changes the ui for usability purposes """

from django.contrib import admin
from .forms import CustomUserChangeForm
from .models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    """This class defines the customs used in the django admin page"""

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """This method takes off the save and continue button when editing an entity"""
        extra_context = extra_context or {} # pragma: no cover
        extra_context["show_save_and_continue"] = False # pragma: no cover
        return super().change_view( # pragma: no cover  
            request, object_id, form_url, extra_context=extra_context
        )

    list_display = ("first_name", "last_name", "is_superuser", "is_leader", "is_member", "is_applicant", "is_none")
    search_fields = ("first_name", "last_name")
    list_editable = ("is_superuser", "is_leader", "is_member", "is_applicant", "is_none")
    list_filter = ("is_superuser", "is_leader", "is_member", "is_applicant", "is_none")
    list_per_page = 10
    form = CustomUserChangeForm


admin.site.unregister(CustomUser)
admin.site.register(CustomUser, UserAdmin)
