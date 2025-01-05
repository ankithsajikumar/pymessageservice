import logging
from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils.timezone import now
from messagesApp.models import Message

logger = logging.getLogger('clearmessages')

class Command(BaseCommand):
    help = "Clear read messages older than 7 days."
 
    def handle(self, *args, **kwargs):
        cutoff_date = now() - timedelta(days=7)
        # Query for messages older than 7 days
        old_messages = Message.objects.filter(timestamp__lt=cutoff_date, is_read=True)
        count = old_messages.count()
 
        if count > 0:
            old_messages.delete()
            logger.info(f"Deleted {count} messages older than 7 days.")
        else:
            logger.info("No messages older than 7 days found.")