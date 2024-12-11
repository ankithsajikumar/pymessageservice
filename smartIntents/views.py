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
 
# Helper to fetch a device by ID
def get_device(device_id):
    return DEVICES.get(device_id)
 
 
@csrf_exempt
def sync_devices(request):
    """Handle SYNC intent."""
    if request.method == "POST":
        data = json.loads(request.body)
        response = {
            "requestId": data.get("requestId"),
            "payload": {
                "agentUserId": "user-123",  # Replace with actual user ID
                "devices": list(DEVICES.values())
            }
        }
        return JsonResponse(response)
 
 
@csrf_exempt
def query_devices(request):
    """Handle QUERY intent."""
    if request.method == "POST":
        data = json.loads(request.body)
        response = {"requestId": data.get("requestId"), "payload": {"devices": {}}}
 
        for device in data["inputs"][0]["payload"]["devices"]:
            device_id = device["id"]
            device_data = get_device(device_id)
            if device_data:
                response["payload"]["devices"][device_id] = device_data["state"]
 
        return JsonResponse(response)
 
 
@csrf_exempt
def execute_devices(request):
    """Handle EXECUTE intent."""
    if request.method == "POST":
        data = json.loads(request.body)
        response = {"requestId": data.get("requestId"), "payload": {"commands": []}}
 
        for command in data["inputs"][0]["payload"]["commands"]:
            devices = command["devices"]
            execution = command["execution"][0]
            command_name = execution["command"]
            params = execution.get("params", {})
 
            for device in devices:
                device_id = device["id"]
                device_data = get_device(device_id)
                if not device_data:
                    continue
 
                # Example: Handle OnOff trait
                if command_name == "action.devices.commands.OnOff":
                    device_data["state"]["on"] = params["on"]
                    response["payload"]["commands"].append({
                        "ids": [device_id],
                        "status": "SUCCESS",
                        "states": device_data["state"]
                    })
 
        return JsonResponse(response)