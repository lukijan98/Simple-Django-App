from django.urls import path
from . import views

urlpatterns = [
	path('create/<str:device_id>/', views.createConfig, name="create")
]