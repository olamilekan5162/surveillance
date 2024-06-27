from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import DeviceState
from core.views import *
import requests

# Create your views here.
ESP32_IP = "http://<esp32-ip>"

def toggle_device(request, device_name, action):
    device = DeviceState.objects.get(name=device_name)
    url = f"{ESP32_IP}/{device_name}/{action}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            device.state = (action == 'on')
            device.save()
    except requests.RequestException:
        pass

    return redirect(moderator_dashboard)

def get_status(request):
    devices = DeviceState.objects.all()
    status = {device.name: device.state for device in devices}
    return JsonResponse(status)
