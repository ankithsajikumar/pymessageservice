from smartDevices.models import Device
from messagesApp.models import Message
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

# Handle query intent
def handle_query(data):
    devices = {}
    for device_id_obj in data['inputs'][0]['payload']['devices']:
        try:
            device_id = device_id_obj['id']
            device = Device.objects.get(device_id=device_id)
            devices[device_id] = {
                "status": "SUCCESS",
                "online": True, # TODO implement device online check
                **device.state
            }
        except Device.DoesNotExist:
            continue

    return JsonResponse({
        "requestId": data["requestId"],
        "payload": {"devices": devices}
    }, status=200)

# Handle execution intent
def handle_execute(data):
    commands = []
    for command in data['inputs'][0]['payload']['commands']:
        for device_command in command['devices']:
            device_id = device_command['id']
            action = command['execution'][0]['command']  # "action.devices.commands.OnOff", etc.

            try:
                device = Device.objects.get(device_id=device_id)
                logger.debug("Device ID: " + device.device_id)
                logger.debug("Action: " + action)
                params = command['execution'][0]['params']
                device.state.update(params)
                device.save()

                # Create message for the execution
                handle_messaging(device, action)

                commands.append({
                    "ids": [device_id],
                    "status": "SUCCESS",
                    "state": device.state
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
            "name": {"name": device.name},
            "willReportState": device.will_report_state,
            "roomHint": device.room
        })

    return JsonResponse({
        "requestId": data["requestId"],
        "payload": {"agentUserId": "admin", "devices": devices}
    }, status=200)

def handle_disconnect(data):
    """Handle DISCONNECT intent."""
    # TODO Clean up user data if needed

def handle_messaging(device, action):
    try:
        message_text= ""
        if action == "action.devices.commands.OnOff":
            action_state = device.state['on']
            message_text= "on" if action_state else "off"
        elif action == "action.devices.commands.BrightnessAbsolute":
            message_text = device.state['brightness']
        message_topic= str(device.device_id) + "/" + str(action)
        Message.objects.create(device_id=device.device_id, topic=message_topic, text=message_text)
    except:
        logger.info("Exception while sending message")
