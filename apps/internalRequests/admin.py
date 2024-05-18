from django.contrib import admin
from .models import Traceability

class TraceabilityAdmin(admin.ModelAdmin):
    """
    Admin options for the Traceability model.
    
    This class defines the administration options for the Traceability model in Django.
    """
    list_display = [field.name for field in Traceability._meta.fields]
    def __init__(self, model, admin_site):
        """
        Initialize TraceabilityAdmin.
        
        Parameters:
        - model: The model class.
        - admin_site: The admin site instance.
        """
        super().__init__(model, admin_site)

admin.site.register(Traceability, TraceabilityAdmin)