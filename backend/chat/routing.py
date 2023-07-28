# chat/routing.py
from django.urls import re_path , path

from . import socket_server
from . import socket_server

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>[\w-]+)/(?P<id_client>[\w-]+)/$", socket_server.ChatConsumer.as_asgi()),
    re_path(r"ws/notification/(?P<id_client>[\w-]+)/$", socket_server.ChatConsumer.as_asgi()),

]
