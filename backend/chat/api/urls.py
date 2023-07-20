from django.urls import path , re_path

from .views import create_conversation , get_all_conversation , get_conversation
# ---------------------------------------------------------------------------- #
#                                  METHOD URL                                  #
# ---------------------------------------------------------------------------- #

urlpatterns = [
    path('conversation/create/', create_conversation, name = "create_conversation"),
    path('conversation/', get_all_conversation, name = "get_all_conversation"),
    re_path(r'^conversation/(?P<uuid>[0-9a-f-]+)/$',get_conversation, name='get_conversation'),
]
