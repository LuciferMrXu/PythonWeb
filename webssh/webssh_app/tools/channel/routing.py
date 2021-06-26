from django.urls import path
from webssh_app.tools.channel import websocket

websocket_urlpatterns = [
    path('webssh/', websocket.WebSSH),
]