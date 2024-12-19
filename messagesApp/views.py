from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import Message
 
@api_view(["POST"])
@csrf_exempt
def receive_message(request):
    """
    Endpoint to receive messages and store them in the database.
    """
    try:
        data = request.data  # Automatically parses JSON data
        message_text = data.get("message", "")
        message_topic = data.get("topic", "")
        message_device_id = data.get("deviceId", "")
        if (not message_text) | (not message_topic) | (not message_device_id):
            return JsonResponse({"status": "error", "message": "No message provided."}, status=400)
        
        # Save the message to the database
        message = Message.objects.create(text=message_text, topic=message_topic, device_id=message_device_id)
        return JsonResponse({"status": "success", "message": "Message received.", "id": message.id}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
@api_view(["POST"])
@csrf_exempt
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
        new_messages = [{"id": msg.id, "deviceId": msg.device_id, "topic": msg.topic, "text": msg.text,"isRead": msg.is_read, "timestamp": msg.timestamp.isoformat()} for msg in messages]
        
        return JsonResponse({"status": "success", "messages": new_messages}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
@api_view(["GET"])
def get_messages(request):
    """
    Endpoint to get all messages.
    """
    try:
        messages = Message.objects.all()
        new_messages = [{"id": msg.id, "deviceId": msg.device_id, "topic": msg.topic, "text": msg.text,"isRead": msg.is_read, "timestamp": msg.timestamp.isoformat()} for msg in messages]
        
        return JsonResponse({"status": "success", "messages": new_messages}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)