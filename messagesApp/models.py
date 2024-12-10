from django.db import models
 
class Message(models.Model):
    text = models.TextField()  # Field to store the message text
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when a message is created