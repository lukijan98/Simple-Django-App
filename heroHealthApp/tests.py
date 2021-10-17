from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
# Create your tests here.
from heroHealthApp.models import Device, Config
from heroHealthApp.test_data import *


class SaveConfigTestCase(APITestCase):



    def testConfigFrontend(self):
        Device.objects.create()
        response = self.client.post("/heroHealthApp/frontend-config/1", data1,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def testConfigDevice(self):
        Device.objects.create()
        response = self.client.post("/heroHealthApp/device-config/1", data2, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def testBoth(self):
        device = Device.objects.create()

        response1 = self.client.post("/heroHealthApp/frontend-config/1", data1, format='json')
        response2 = self.client.post("/heroHealthApp/device-config/1", data2, format='json')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(Config.objects.filter(device=device).count(), 2)
        self.assertEqual(Config.objects.filter(device=device,active=True).count(), 1)
        self.assertEqual(Config.objects.filter(device=device, active=False).count(), 1)
