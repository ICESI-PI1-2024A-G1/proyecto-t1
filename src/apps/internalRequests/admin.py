from django.contrib import admin
from .models import Traceability

class TraceabilityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Traceability._meta.fields]

admin.site.register(Traceability, TraceabilityAdmin)