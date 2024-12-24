from django.contrib import admin

from .models import Message

@admin.action(description="Mark selected messages as unread")
def make_unread(modeladmin, request, queryset):
    queryset.update(is_read=False)

class MessageAdmin(admin.ModelAdmin):
    ordering = ['timestamp']
    list_display = ["id", "topic", "text"]
    search_fields = ['topic', 'text']
    list_filter = ['topic']
    actions = [make_unread]

admin.site.register(Message, MessageAdmin)