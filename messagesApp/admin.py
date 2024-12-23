from django.contrib import admin

from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "topic", "text"]
    search_fields = ['topic', 'text']
    list_filter = ['topic']

admin.site.register(Message, MessageAdmin)