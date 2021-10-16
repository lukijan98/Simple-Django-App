from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ConfigFrontendSerializer, ConfigDeviceSerializer

from .models import Config, Device
# Create your views here.

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def frontendConfig(request, device_id):
	config = Config.objects.get(device=device_id, active=True)
	device = Device.objects.get(id=device_id)
	serializer = None
	if config is None:
		serializer = ConfigFrontendSerializer(data=request.data, context={'device': device})
	else:
		serializer = ConfigFrontendSerializer(instance=config, data=request.data, context={'device': device})
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def deviceConfig(request, device_id):
	config = Config.objects.get(device=device_id, active=True)
	device = Device.objects.get(id=device_id)
	serializer = None
	if config is None:
		serializer = ConfigDeviceSerializer(data=request.data, context={'device': device})
	else:
		serializer = ConfigDeviceSerializer(instance=config, data=request.data, context={'device': device})
	if serializer.is_valid():
		 serializer.save()
		 print("uSao")

	serializer.is_valid()
	return Response(serializer.validated_data)