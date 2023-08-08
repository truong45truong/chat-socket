from django.urls import path , include
from django.conf.urls.static import static

urlpatterns = [
    path('api/',include('chat_user.user.urls')) ,
    path('api/',include('chat_user.chat.urls')) ,
]
