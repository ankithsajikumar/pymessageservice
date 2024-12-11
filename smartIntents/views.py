from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
 
# Mock database for devices (replace with your actual database queries)
DEVICES = {
    "device-1": {
        "id": "device-1",
        "type": "action.devices.types.LIGHT",
        "traits": ["action.devices.traits.OnOff"],
        "name": {
            "defaultNames": ["Smart Light"],
            "name": "Bedroom Light",
            "nicknames": ["Night Light"]
        },
        "willReportState": False,
        "state": {
            "on": False
        }
    }
}
 
@csrf_exempt
def smart_home_fulfillment(request):
    """Handle all Smart Home intents."""
    if request.method == "POST":
        data = json.loads(request.body)
        intent = data["inputs"][0]["intent"]
        request_id = data.get("requestId", "")
 
        if intent == "action.devices.SYNC":
            return handle_sync(request_id)
        elif intent == "action.devices.QUERY":
            return handle_query(request_id, data)
        elif intent == "action.devices.EXECUTE":
            return handle_execute(request_id, data)
        elif intent == "action.devices.DISCONNECT":
            return handle_disconnect(request_id)
        else:
            return JsonResponse({"error": "Unknown intent"}, status=400)
 
    return JsonResponse({"error": "Invalid request method"}, status=405)
 
def handle_sync(request_id):
    """Handle SYNC intent."""
    return JsonResponse({
        "requestId": request_id,
        "payload": {
            "agentUserId": "user-123",  # Replace with actual user ID
            "devices": list(DEVICES.values())
        }
    })
 
def handle_query(request_id, data):
    """Handle QUERY intent."""
    devices = {}
    for device in data["inputs"][0]["payload"]["devices"]:
        device_id = device["id"]
        if device_id in DEVICES:
            devices[device_id] = DEVICES[device_id]["state"]
 
    return JsonResponse({
        "requestId": request_id,
        "payload": {"devices": devices}
    })
 
def handle_execute(request_id, data):
    """Handle EXECUTE intent."""
    commands = []
    for command in data["inputs"][0]["payload"]["commands"]:
        for device in command["devices"]:
            device_id = device["id"]
            execution = command["execution"][0]
 
            if device_id in DEVICES:
                # Example: Handle OnOff command
                if execution["command"] == "action.devices.commands.OnOff":
                    DEVICES[device_id]["state"]["on"] = execution["params"]["on"]
 
                commands.append({
                    "ids": [device_id],
                    "status": "SUCCESS",
                    "states": DEVICES[device_id]["state"]
                })
 
    return JsonResponse({
        "requestId": request_id,
        "payload": {"commands": commands}
    })
 
def handle_disconnect(request_id):
    """Handle DISCONNECT intent."""
    # Clean up user data if needed
    return JsonResponse({"requestId": request_id, "status": "OK"})