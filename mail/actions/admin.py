from django.contrib import admin

from .models import Email


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
<<<<<<< codex/implement-email-client-server-with-django-x9147v
    list_display = ('id', 'sender', 'recipient', 'subject', 'is_read', 'sender_deleted', 'recipient_deleted', 'created_at')
    list_filter = ('is_read', 'sender_deleted', 'recipient_deleted', 'created_at')
=======
    list_display = ('id', 'sender', 'recipient', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
>>>>>>> main
    search_fields = ('subject', 'sender__username', 'recipient__username')
