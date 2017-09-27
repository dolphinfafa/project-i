from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'email', 'text', 'number', 'created_at', 'modified_at', 'lang')
    list_display = ('number', 'email', 'text')
