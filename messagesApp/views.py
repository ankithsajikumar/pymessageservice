import logging
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from .models import Message

logger = logging.getLogger(__name__)
    
@api_view(["POST"])
@permission_required('messagesApp.view_message', raise_exception=True)
@permission_required('messagesApp.change_message', raise_exception=True)
def poll_messages(request):
    """
    Endpoint to poll messages that are not read.
    """
    try:
        data = request.data
        messages_read = data.get("messagesRead", "")
        if messages_read:
            Message.objects.filter(id__in=messages_read).update(is_read=True)
        messages = Message.objects.filter(is_read=False)
        new_messages = [
            {
                "id": msg.id,
                "deviceId": msg.device_id,
                "topic": msg.topic,
                "text": msg.text,
                "isRead": msg.is_read,
                "timestamp": msg.timestamp.isoformat()
            } for msg in messages
        ]
        
        return JsonResponse({"status": "success", "messages": new_messages}, status=200)
    except Exception as e:
        logger.error("Error occurred while polling messages: " + str(e))
        return JsonResponse({"status": "error", "message": "Check logs for details"}, status=500)
