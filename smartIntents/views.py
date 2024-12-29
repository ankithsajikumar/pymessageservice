import logging
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from .services import handle_execute, handle_query, handle_sync, handle_disconnect

logger = logging.getLogger(__name__)
 
@api_view(["POST"])
@permission_required('messagesApp.add_message', raise_exception=True)
@permission_required('smartDevices.change_device', raise_exception=True)
def smart_home_fulfillment(request):
    try:
        data = request.data

        # Extract the intent from the request
        intent = data.get('inputs', [])[0].get('intent')
        logger.debug("Intent: " + intent)

        # Route to the appropriate handler based on the intent
        if intent == "action.devices.QUERY":
            return handle_query(data)
        elif intent == "action.devices.EXECUTE":
            return handle_execute(data)
        elif intent == "action.devices.SYNC":
            return handle_sync(data, request.user)
        elif intent == "action.devices.DISCONNECT":
            return handle_disconnect(data)
        else:
            return JsonResponse({"error": "Intent not recognized"}, status=400)

    except Exception as e:
        logger.error("Exception caught while processing intent: " + str(e))
        return JsonResponse({"error": "Intent processing failed, check logs for details"}, status=500)
