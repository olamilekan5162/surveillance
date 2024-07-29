from django.shortcuts import render, redirect
from core.cam import *
from django.http.response import StreamingHttpResponse, HttpResponse
from .models import *
from accounts.models import Visitor, Moderator
from motion.models import DeviceState
from django.contrib.auth.models import User
import os

# Update the URL with your NVR's stream URL
camera1 = IpWebCam("rtsp://admin:surveillance123@192.168.1.176:554/Streaming/Channels/101")
camera2 = IpWebCam("rtsp://admin:surveillance123@192.168.1.176:554/Streaming/Channels/201")

def index(request):
    return render(request, 'core/index.html')

def moderator_dashboard(request):
    user = request.user    
    recordings = Recording.objects.all()
    visitor = Visitor.objects.all()
    devices = DeviceState.objects.all()

    if user.is_authenticated:
        is_moderator = Moderator.objects.filter(user=user).exists()
        context = {
            'recordings': recordings,
            'visitor': visitor, 
            'devices': devices,
            'is_moderator': is_moderator
        }
        return render(request, 'core/moderator_dashboard.html', context)
    else:
        return HttpResponse('Your must log in first to view this page <br> <a href="/">Go Back</a>')

def visitor_dashboard(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'core/visitor_dashboard.html')
    else:
        return HttpResponse('Your must log in first to view this page <br> <a href="/">Go Back</a>')

def gen(cam):
    while True:
        frame = cam.get_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def webcam1(request):
    return StreamingHttpResponse(gen(camera1),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def webcam2(request):
    return StreamingHttpResponse(gen(camera2),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

# def start_recording(request):
#     camera1.start_recording()
#     camera2.start_recording()
#     return redirect('admin')

# def stop_recording(request):
#     filepath1 = camera1.stop_recording()
#     filepath2 = camera2.stop_recording()
#     Recording.objects.create(file_path=filepath1)
#     Recording.objects.create(file_path=filepath2)
#     return redirect('admin')

def recordings(request):
    recordings = Recording.objects.all()
    return render(request, 'camera/recordings.html', {'recordings': recordings})

def play_recording(request, recording_id):
    recording = Recording.objects.get(id=recording_id)
    file_path = recording.file_path
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="video/avi")
        response['Content-Disposition'] = f'inline; filename={os.path.basename(file_path)}'
        return response
    
def authorize(request, pk):
    visitor = Visitor.objects.get(id=pk)
    visitor.is_authorized = True
    visitor.save()
    return redirect(moderator_dashboard)

def unauthorize(request, pk):
    visitor = Visitor.objects.get(id=pk)
    visitor.is_authorized = False
    visitor.save()
    return redirect(moderator_dashboard)
