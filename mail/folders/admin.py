from django.contrib import admin

from .models import Folder


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'system_name', 'created_at')
    list_filter = ('system_name',)
    search_fields = ('user__username', 'name')
