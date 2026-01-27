from django.contrib import admin
from .models import DashboardCache

@admin.register(DashboardCache)
class DashboardCacheAdmin(admin.ModelAdmin):
    list_display = ('cache_key', 'created_at', 'expires_at')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('cache_key',)
    readonly_fields = ('created_at',)
    
    def has_add_permission(self, request):
        # Don't allow adding cache entries manually
        return False