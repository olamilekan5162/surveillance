from django.shortcuts import render, redirect
from core.cam import *
from django.http.response import StreamingHttpResponse, HttpResponse
from . models import *
from accounts.models import Visitor, Moderator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import os

camera = IpWebCam("http://192.168.112.205:8080/shot.jpg")

# Create your views here.
def index(request):
    return render(request, 'core/index.html')


def moderator_dashboard(request):
        
        user = request.user    
        recordings = Recording.objects.all()
        visitor = Visitor.objects.all()
        if user.is_authenticated:
            is_moderator = Moderator.objects.filter(user=user).exists()

            context = {'recordings': recordings,
                       'visitor': visitor, 
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
      yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
      
def webcam(request):
   return StreamingHttpResponse(gen(camera),
                                content_type='multipart/x-mixed-replace; boundary=frame')

# def start_recording(request):
#     camera.start_recording()
#     return redirect('admin')

# def stop_recording(request):
#     filepath = camera.stop_recording()
#     Recording.objects.create(file_path=filepath)
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
    
def authorize(request,pk):
    visitor = Visitor.objects.get(id=pk)
    if request.method == 'POST':
        visitor.is_authorized = True
        visitor.save()
        return redirect(moderator_dashboard)

def unauthorize(request,pk):
    visitor = Visitor.objects.get(id=pk)
    if request.method == 'POST':
        visitor.is_authorized = False
        visitor.save()
        return redirect(moderator_dashboard)