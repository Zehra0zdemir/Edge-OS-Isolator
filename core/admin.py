from django.contrib import admin
from .models import SystemAuditLog

@admin.register(SystemAuditLog)
class SystemAuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'action_type', 'target_username', 'status')
    list_filter = ('action_type', 'status')
    search_fields = ('target_username', 'details')
    readonly_fields = ('timestamp', 'action_type', 'target_username', 'status', 'details')

    # Security measure: Prevent manual log tampering from the admin dashboard
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False