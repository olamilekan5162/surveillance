from django.urls import path
from . import views

urlpatterns = [
    path('moderator_reg/',views.moderator_reg, name='moderator_reg'),
    path('moderator_login/',views.moderator_login, name='moderator_login'),
    path('moderator_logout/',views.moderator_logout, name='moderator_logout'),
    path('visitor_reg/',views.visitor_reg, name='visitor_reg'),
    path('visitor_login/',views.visitor_login, name='visitor_login'),
    path('visitor_logout/',views.visitor_logout, name='visitor_logout'),
]