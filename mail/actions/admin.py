from django.contrib import admin

from .models import Email


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'recipient', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('subject', 'sender__username', 'recipient__username')
