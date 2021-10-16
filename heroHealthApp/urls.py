from django.urls import path
from . import views

urlpatterns = [
	path('frontend-config/<str:device_id>', views.frontendConfig, name="frontend-config"),
	path('device-config/<str:device_id>', views.deviceConfig, name="device-config"),
	path('config-list/', views.configList, name="config-list"),
	path('config-detail/<str:id>/', views.configDetail, name="config-detail"),
]