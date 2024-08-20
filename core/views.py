from django.shortcuts import render, redirect
from core.cam import *
from django.http.response import StreamingHttpResponse, HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str
from .models import *
from accounts.models import Visitor, Moderator
from motion.models import DeviceState
from django.contrib.auth.models import User
import os

# Update the URL with your NVR's stream URL
camera1 = IpWebCam("rtsp://admin:surveillance123@192.168.1.176:554/Streaming/Channels/101")
camera2 = IpWebCam("rtsp://admin:surveillance123@192.168.1.176:554/Streaming/Channels/101")
camera3 = IpWebCam("rtsp://admin:surveillance123@192.168.1.176:554/Streaming/Channels/101")
camera4 = IpWebCam("rtsp://admin:surveillance123@192.168.1.176:554/Streaming/Channels/101")

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

def webcam3(request):
    return StreamingHttpResponse(gen(camera3),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
def webcam4(request):
    return StreamingHttpResponse(gen(camera4),
                                 content_type='multipart/x-mixed-replace; boundary=frame')



def start_recording(request):
    pass
    # camera1.start_recording()
    # camera2.start_recording()
    # camera3.start_recording()
    # camera4.start_recording()
    # return redirect('admin')

def stop_recording(request):
    pass
    # camera1.stop_recording()
    # camera2.stop_recording()
    # camera3.stop_recording()
    # camera4.stop_recording()
    # return redirect('admin')

def recordings(request):
    recordings = Recording.objects.all()
    return render(request, 'camera/recordings.html', {'recordings': recordings})

def play_recording(request, recording_id):
    recording = Recording.objects.get(id=recording_id)
    video_data = recording.video_data
    response = HttpResponse(video_data, content_type="video/mp4")
    response['Content-Disposition'] = f'inline; filename=recording_{recording_id}.mp4'
    return response

    
# def play_recording(request, recording_id):
#     recording = get_object_or_404(Recording, pk=recording_id)
#     file_path = recording.file_path

#     if not os.path.exists(file_path):
#         return HttpResponseNotFound("File not found")

#     file_size = os.path.getsize(file_path)
#     range_header = request.headers.get('Range', None)

#     if range_header:
#         byte_range = range_header.strip().split('=')[-1]
#         start, end = byte_range.split('-')
#         start = int(start)
#         end = int(end) if end else file_size - 1
        
#         with open(file_path, 'rb') as f:
#             f.seek(start)
#             data = f.read(end - start + 1)

#         response = HttpResponse(data, status=206, content_type='video/mp4')
#         response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
#         response['Content-Length'] = str(end - start + 1)
#         response['Accept-Ranges'] = 'bytes'
#     else:
#         with open(file_path, 'rb') as f:
#             response = HttpResponse(f.read(), content_type='video/mp4')
#         response['Content-Length'] = str(file_size)
#         response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'

#     response['Cache-Control'] = 'no-cache'
#     response['Pragma'] = 'no-cache'

#     return response

    
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
