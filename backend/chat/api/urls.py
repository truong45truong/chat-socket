from django.urls import path , re_path

from .views import create_conversation , get_all_conversation , get_conversation
from . views import checked_conversation , create_group , get_all_group_user , chat_group
from . views import get_all_notification , create_notification , update_seem_notification
from . views import chat_conversation , seem_conversation
# ----------------------------------------------create_group------------------------------ #
#                                  METHOD URL                                  #
# ---------------------------------------------------------------------------- #

urlpatterns = [
    path('conversation/create/', create_conversation, name = "create_conversation"),
    path('conversation/chat/', chat_conversation, name = "create_conversation"),
    path('group/create/', create_group, name = "create_group"),
    path('group/chat/', chat_group, name = "chat_group"),
    path('group/', get_all_group_user, name = "get_all_group_user"),
    path('conversation/', get_all_conversation, name = "get_all_conversation"),
    path('conversation/seem/', seem_conversation, name = "seem_conversation"),

    path('conversation/check/', checked_conversation, name = "check_conversation"),
    path('notification/', get_all_notification, name = "get_all_notification"),
    path('notification/create/', create_notification, name = "create_notification"),
    path('notification/seem/', update_seem_notification, name = "update_seem_notification"),
    re_path(r'^conversation/(?P<uuid>[0-9a-f-]+)/$',get_conversation, name='get_conversation'),

]
