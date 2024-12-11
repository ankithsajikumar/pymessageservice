from django.db import models
 
class Trait(models.Model):
    name = models.CharField(max_length=100)  # e.g., "OnOff", "Brightness"
 
    def __str__(self):
        return self.name
 
 
class State(models.Model):
    key = models.CharField(max_length=100)  # e.g., "on", "brightness", "online"
    value = models.CharField(max_length=255)  # Store the state value as a string (convert as needed)
 
    def __str__(self):
        return f"{self.key}: {self.value}"
 
 
class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    device_type = models.CharField(max_length=100)
    traits = models.ManyToManyField(Trait, related_name="devices")  # Many-to-many relationship
    name = models.CharField(max_length=100)
    room = models.CharField(max_length=100, null=True, blank=True)
    will_report_state = models.BooleanField(default=True)
    states = models.ManyToManyField(State, related_name="devices")  # Many-to-many relationship
 
    def __str__(self):
        return self.name