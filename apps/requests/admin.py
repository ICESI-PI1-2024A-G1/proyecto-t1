from django.contrib import admin
from .models import SharePoint

class SharePointAdmin(admin.ModelAdmin):
    """
    Admin configuration for the SharePoint model.

    This configuration determines how the SharePoint model is displayed and interacted with in the Django admin interface.
    """
    list_display = [field.name for field in SharePoint._meta.fields]

admin.site.register(SharePoint, SharePointAdmin)