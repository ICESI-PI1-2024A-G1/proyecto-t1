from django.contrib import admin
from .models import SharePoint

class SharePointAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SharePoint._meta.fields]

admin.site.register(SharePoint, SharePointAdmin)