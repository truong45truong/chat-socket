from django.urls import path
from . import views

urlpatterns = [
    path("chat/socket/", views.chat, name="room"),
]