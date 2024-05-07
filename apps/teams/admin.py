from django.contrib import admin
from .models import Team

class TeamAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Team._meta.fields]

admin.site.register(Team, TeamAdmin)