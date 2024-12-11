import json
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Device, Trait, State
from django.views.decorators.csrf import csrf_exempt
 
@csrf_exempt
def create_device(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
 
            # Create or get the device
            device, created = Device.objects.get_or_create(
                device_id=data['device_id'],
                defaults={
                    'device_type': data['device_type'],
                    'name': data['name'],
                    'room': data.get('room', None),
                    'will_report_state': data.get('will_report_state', True),
                }
            )
 
            # Add traits
            if 'traits' in data:
                for trait_name in data['traits']:
                    trait, _ = Trait.objects.get_or_create(name=trait_name)
                    device.traits.add(trait)
 
            # Add states
            if 'state' in data:
                for key, value in data['state'].items():
                    state, _ = State.objects.get_or_create(key=key, value=str(value))
                    device.states.add(state)
 
            device.save()
 
            return JsonResponse({'message': 'Device created successfully!', 'device_id': device.device_id}, status=201)
 
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
#to-do
# Get Device
def get_device(request, device_id):
    if request.method == "GET":
        try:
            device = get_object_or_404(Device, device_id=device_id)
            return JsonResponse(model_to_dict(device), status=200)
        except Device.DoesNotExist:
            return JsonResponse({"error": "Device not found"}, status=404)
 
#to-do
# Update Device
@csrf_exempt
def update_device(request, device_id):
    if request.method == "PUT":
        data = json.loads(request.body)
 
        try:
            device = get_object_or_404(Device, device_id=device_id)
            device.name = data.get("name", device.name)
            device.device_type = data.get("device_type", device.device_type)
            device.room = data.get("room", device.room)
 
            # Update traits
            device.traits.clear()
            traits = data.get("traits", [])
            for trait_name in traits:
                trait = Trait.objects.get_or_create(name=trait_name)
                device.traits.add(trait)
 
            device.save()
            return JsonResponse(device.name, status=200)
 
        except Device.DoesNotExist:
            return JsonResponse({"error": "Device not found"}, status=404)
 
 
# Delete Device
@csrf_exempt
def delete_device(request, device_id):
    if request.method == "DELETE":
        try:
            device = get_object_or_404(Device, device_id=device_id)
            device.delete()
            return JsonResponse({"message": "Device deleted successfully"}, status=200)
        except Device.DoesNotExist:
            return JsonResponse({"error": "Device not found"}, status=404)