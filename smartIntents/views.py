from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from smartDevices.models import Device, State
 
@csrf_exempt
def smart_home_fulfillment(request):
    try:
        data = json.loads(request.body)

        # Extract the intent from the request
        intent = data.get('inputs', [])[0].get('intent')

        # Route to the appropriate handler based on the intent
        if intent == "action.devices.QUERY":
            return handle_query(data)
        elif intent == "action.devices.EXECUTE":
            return handle_execute(data)
        elif intent == "action.devices.SYNC":
            return handle_sync(data)
        elif intent == "action.devices.DISCONNECT":
            return handle_disconnect(data)
        else:
            return JsonResponse({"error": "Intent not recognized"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
 
# Handle query intent
def handle_query(data):
    devices = []
    for device_id in data['inputs'][0]['payload']['devices']:
        try:
            device = Device.objects.get(device_id=device_id)
            device_state = {"on": False, "brightness": 50}  # Example state, adjust based on your model

            devices.append({
                "id": device.device_id,
                "state": device_state
            })
        except Device.DoesNotExist:
            continue

    return JsonResponse({
        "requestId": data["requestId"],
        "payload": {"devices": devices}
    }, status=200)

# Handle execute intent
def handle_execute(data):
    commands = []
    for command in data['inputs'][0]['payload']['commands']:
        for device_command in command['devices']:
            device_id = device_command['id']
            action = command['execution'][0]['command']  # "action.devices.commands.OnOff", etc.

            try:
                device = Device.objects.get(device_id=device_id)

                if action == "action.devices.commands.OnOff":
                    new_state = "on" if device_command['execution'][0]['params']['on'] else "off"
                    device_state = {"on": new_state}
                    state_obj, created = State.objects.get_or_create(key="on", value=new_state)
                    device.states.add(state_obj)
                    device.save()

                commands.append({
                    "ids": [device_id],
                    "status": "SUCCESS",
                    "state": device_state
                })
            except Device.DoesNotExist:
                commands.append({
                    "ids": [device_id],
                    "status": "ERROR"
                })

    return JsonResponse({
        "requestId": data["requestId"],
        "payload": {"commands": commands}
    }, status=200)

# Handle sync intent
def handle_sync(data):
    devices = []
    all_devices = Device.objects.all()

    for device in all_devices:
        devices.append({
            "id": device.device_id,
            "type": device.device_type,
            "traits": [trait.name for trait in device.traits.all()],
            "name": {"defaultNames": [device.name]},
            "willReportState": device.will_report_state,
            "roomHint": device.room
        })

    return JsonResponse({
        "requestId": data["requestId"],
        "payload": {"agentUserId": "admin", "devices": devices}
    }, status=200)

def handle_disconnect(data):
    """Handle DISCONNECT intent."""
    # Clean up user data if needed
    return JsonResponse({"requestId":  data["requestId"], "status": "OK"})