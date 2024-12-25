import uuid
from django.db import models
 
class Message(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_id = models.CharField(max_length=100)
    topic= models.TextField()
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)  # Automatically set when a message is created/updated