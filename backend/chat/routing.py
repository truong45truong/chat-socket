# chat/routing.py
from django.urls import re_path , path

from . import socket_server

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", socket_server.ChatConsumer.as_asgi()),
]
