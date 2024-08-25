from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import DeviceState
from core.views import *
import requests

# Create your views here.
ESP32_IP1 = "http://192.168.73.19"
ESP32_IP2 = "http://192.168.228.123"
ESP32_IP3 = "http://192.168.228.123"

def toggle_device(request, device_name, action):
    device = DeviceState.objects.get(name=device_name)
    if device_name == "alarm1":
        url = f"{ESP32_IP1}/{device.name}/{action}"
    elif device_name == "alarm2":
        url = f"{ESP32_IP2}/{device.name}/{action}"
    elif device_name == "floodlight1" or device_name == "floodlight2":
        url = f"{ESP32_IP3}/{device.name}/{action}"     

    try:
        response = requests.get(url)
        if response.status_code == 200:
            device.state = (action == 'on')
            device.save()
        else:
            print(f"Failed to toggle device. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")

    return redirect(moderator_dashboard)

def get_status(request):
    devices = DeviceState.objects.all()
    status = {device.name: device.state for device in devices}
    return JsonResponse(status)

def motion(request):
    return render(request, 'core/motion.html')
