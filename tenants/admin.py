from django.contrib import admin
from .models import Tenant

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'created_at')
    search_fields = ('name', 'domain')
    readonly_fields = ('created_at',)
