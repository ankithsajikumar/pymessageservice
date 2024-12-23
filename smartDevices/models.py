from django.db import models
from jsonfield import JSONField
 
class Trait(models.Model):
    name = models.CharField(max_length=100)  # e.g., "OnOff", "Brightness"
 
    def __str__(self):
        return self.name
 
class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    device_type = models.CharField(max_length=100)
    traits = models.ManyToManyField(Trait, related_name="devices")  # Many-to-many relationship
    name = models.CharField(max_length=100)
    room = models.CharField(max_length=100, null=True, blank=True)
    will_report_state = models.BooleanField(default=True)
    state = JSONField(default=dict)
 
    def __str__(self):
        return self.name
