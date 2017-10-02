from django.contrib import admin
from .models import Retail


@admin.register(Retail)
class RetailAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'modified_at')
    list_display = ('name', 'description')
