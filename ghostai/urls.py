from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard', views.dashboard, name='dashboard_alias'),
    path('voice', views.voice, name='voice'),
    path('api/telemetry', views.get_telemetry, name='telemetry'),
    path('api/missions', views.get_missions, name='missions'),
    path('api/command', views.handle_command, name='command'),
    path('api/tts', views.tts_placeholder, name='tts'),
]
