from django.urls import path
from . import views

urlpatterns = [
    path('toggle/<str:device_name>/<str:action>/', views.toggle_device, name='toggle_device'),
    path('status/', views.get_status, name='get_status'),
]
