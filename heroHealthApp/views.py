from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ConfigFrontendSerializer, ConfigDeviceSerializer, ConfigSerializer

from .models import Config, Device


# Create your views here.

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def frontendConfig(request, device_id):
    try:
        config = Config.objects.get(device=device_id, active=True)
    except Config.DoesNotExist:
        config = None
    device = Device.objects.get(id=device_id)
    serializer = None
    if config is None:
        serializer = ConfigFrontendSerializer(data=request.data, context={'device': device})
    else:
        serializer = ConfigFrontendSerializer(instance=config, data=request.data, context={'device': device})
    if serializer.is_valid():
        config = serializer.save()
        serializer = ConfigFrontendSerializer(config)
        return Response(serializer.data)
    return Response("Failed")


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def deviceConfig(request, device_id):
    try:
        config = Config.objects.get(device=device_id, active=True)
    except Config.DoesNotExist:
        config = None
    device = Device.objects.get(id=device_id)
    if config is None:
        serializer = ConfigDeviceSerializer(data=request.data, context={'device': device})
    else:
        serializer = ConfigDeviceSerializer(instance=config, data=request.data, context={'device': device})
    if serializer.is_valid():
        config = serializer.save()
        serializer = ConfigFrontendSerializer(config)
        return Response(serializer.data)

    return Response("Failed")


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def configList(request):
	configs = Config.objects.all().order_by('-id')
	serializer = ConfigFrontendSerializer(configs, many=True)
	return Response(serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def configDetail(request, id):
	configs = Config.objects.get(id=id)
	serializer = ConfigFrontendSerializer(configs, many=False)
	return Response(serializer.data)