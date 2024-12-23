from django.contrib import admin
from .models import Device, Trait

class DeviceAdmin(admin.ModelAdmin):
    list_display = ["name", "device_id", "device_type"]
    search_fields = ['name', 'device_id', 'device_type']

admin.site.register(Device, DeviceAdmin)
admin.site.register(Trait)
