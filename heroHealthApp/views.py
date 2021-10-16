from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import permissions

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ConfigFrontendSerializer

from .models import Config, Device
# Create your views here.

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def createConfig(request, device_id):
	config = Config.objects.filter(device=device_id).order_by('-id').first()
	device = Device.objects.get(id=device_id)
	serializer = None
	if config is None:
		serializer = ConfigFrontendSerializer(data=request.data, context={'device':device})
	else:
		serializer = ConfigFrontendSerializer(instance=config, data=request.data, context={'device':device})

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)
