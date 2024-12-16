from django.contrib import admin
from .models import Device, State, Trait

admin.site.register(Device)
admin.site.register(State)
admin.site.register(Trait)
