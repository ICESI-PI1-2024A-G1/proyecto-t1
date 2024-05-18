from django.contrib import admin
from .models import Team

class TeamAdmin(admin.ModelAdmin):
    """
    Admin class for Team model.

    This class customizes the display of Team model in the Django admin interface.

    Attributes:
        list_display (list): A list of field names to be displayed in the admin list view.
    """
    list_display = [field.name for field in Team._meta.fields]

admin.site.register(Team, TeamAdmin)