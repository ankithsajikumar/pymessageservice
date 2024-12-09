from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import json
 
# Simulate a database or in-memory store for messages
message_store = []
latest_id = 0
 
@api_view(["POST"])
@csrf_exempt  # Only use CSRF exemption if needed; ensure proper security measures
def receive_message(request):
    """
    Endpoint to receive messages from external sources (like Express).
    """
    global latest_id
    try:
        data = json.loads(request.body)
        message = data.get("message", "")
        if message:
            latest_id += 1
            message_store.append({"id": latest_id, "text": message})
            return JsonResponse({"status": "success", "message": "Message received."}, status=200)
        else:
            return JsonResponse({"status": "error", "message": "No message provided."}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
 
 
@api_view(["GET"])
def get_messages(request):
    """
    Endpoint to return messages since a given ID.
    """
    try:
        since_id = int(request.GET.get('sinceId', 0))  # Default to 0 if not provided
        new_messages = [msg for msg in message_store if msg['id'] > since_id]
        return JsonResponse({"status": "success", "newMessages": new_messages, "latestId": latest_id}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)