from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from .forms import CustomUserChangeForm 
from .models import CustomUser
# Register your models here.
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
    list_display=('first_name', 'last_name', 'is_superuser', 'is_leader')
    search_fields=('first_name','last_name')
    list_editable=('is_superuser', 'is_leader')
    list_filter=('is_superuser', 'is_leader')
    list_per_page=10
    exclude=('last_login', 'groups', 'user_permissions', 'is_staff')
    form = CustomUserChangeForm

admin.site.unregister(CustomUser)
admin.site.register(CustomUser, UserAdmin)