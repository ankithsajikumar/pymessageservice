from django.http import JsonResponse
from .models import Device, Trait, State
from django.views.decorators.csrf import csrf_exempt
 
@csrf_exempt
def create_device(request):
    if request.method == 'POST':
        try:
            import json
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