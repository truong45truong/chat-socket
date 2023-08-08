from django.urls import path ,re_path
from .views import view_api
urlpatterns = [

    #CONVERSATION   
    re_path(r'^conversation/(?P<uuid>[0-9a-f-]+)/$',view_api.get_conversation, name='get_conversation'),
    path('conversation/', view_api.get_all_conversation, name = "get_all_conversation"),
    path('conversation/create/', view_api.create_conversation, name = "create_conversation"),
    path('conversation/chat/', view_api.chat_conversation, name = "create_conversation"),
    path('conversation/seem/', view_api.seem_conversation, name = "seem_conversation"),
    path('conversation/check/', view_api.checked_conversation, name = "check_conversation"),

    #GROUP
    path('group/', view_api.get_all_group_user, name = "get_all_group_user"),
    path('group/create/', view_api.create_group, name = "create_group"),
    path('group/chat/', view_api.chat_group, name = "chat_group"),

    # NOTIFICATION
    path('notification/', view_api.get_all_notification, name = "get_all_notification"),
    path('notification/create/', view_api.create_notification, name = "create_notification"),
    path('notification/seem/', view_api.update_seem_notification, name = "update_seem_notification"),
    
]