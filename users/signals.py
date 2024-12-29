from oauth2_provider.signals import app_authorized
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

@receiver(app_authorized)
def add_user_to_token(sender, request, token, **kwargs):
    application = token.application
    if "message-client" in application.name:
        logger.info("User added to token for app: " + str(application.name))
        service_user = application.user
        token.user = service_user
        token.save()