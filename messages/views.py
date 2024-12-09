from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import json
 
# Simulate a database or in-memory store for messages
message_store = []
 
@api_view(["POST"])
@csrf_exempt  # Only use CSRF exemption if needed; ensure proper security measures
def receive_message(request):
    """
    Endpoint to receive messages from Node.js or other clients.
    """
    try:
        data = json.loads(request.body)
        message = data.get("message", "")
        if message:
            message_store.append({"message": message})
            return JsonResponse({"status": "success", "message": "Message received."}, status=200)
        else:
            return JsonResponse({"status": "error", "message": "No message provided."}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
 
 
@api_view(["GET"])
def get_messages(request):
    """
    Endpoint to send messages to Node.js or other clients.
    """
    return JsonResponse({"status": "success", "messages": message_store}, status=200)