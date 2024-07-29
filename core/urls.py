from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('moderator_dashboard/', views.moderator_dashboard, name='moderator_dashboard'),
    path('visitor_dashboard/', views.visitor_dashboard, name='visitor_dashboard'),
    path('webcam1/', views.webcam1, name='webcam1'),
    path('webcam2/', views.webcam2, name='webcam2'),
    # path('start_recording/', views.start_recording, name='start_recording'),
    # path('stop_recording/', views.stop_recording, name='stop_recording'),
    path('recordings/', views.recordings, name='recordings'),
    path('play_recording/<int:recording_id>/', views.play_recording, name='play_recording'),
    path('authorize/<str:pk>', views.authorize, name='authorize'),
    path('unauthorize/<str:pk>', views.unauthorize, name='unauthorize'),

]