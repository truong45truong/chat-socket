from django.urls import path ,re_path
from . import views
urlpatterns = [
    path("chat/socket/", views.chat, name="room"),
]