from rest_framework.decorators import api_view,authentication_classes
from chat_base.core.middlewares.authenticate import CustomAuthentication
from ..services.service_chat import ChatService
from ..services.service_notification import NotificationService
from ..services.service_group import GroupService


# ---------------------------------------------------------------------------- #
#                                 CONVERSATION                                 #
# ---------------------------------------------------------------------------- #
@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def create_conversation(request):
    chatService = ChatService()
    return chatService.create_conversation(request)

@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def get_all_conversation(request):
    chatService = ChatService()
    return chatService.get_all_conversation(request)
@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def get_conversation(request , uuid):
    chatService = ChatService()
    return chatService.get_conversation(request,uuid)

@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def chat_conversation(request):
    chatService = ChatService()
    return chatService.chat_conversation(request)

@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def seem_conversation(request):
    chatService = ChatService()
    return chatService.seem_conversation(request)

@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def checked_conversation(request):
    chatService = ChatService()
    return chatService.check_conversation(request)

# ---------------------------------------------------------------------------- #
#                                  GROUP CHAT                                  #
# ---------------------------------------------------------------------------- #

@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def chat_group(request):
    groupService = GroupService()
    return groupService.chat_group(request)

@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def create_group(request):
    groupService = GroupService()
    return groupService.create_group(request)

@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def get_all_group_user(request):
    groupService = GroupService()
    return groupService.get_all_group_user(request)

# ---------------------------------------------------------------------------- #
#                                 NOTIFICATION                                 #
# ---------------------------------------------------------------------------- #

@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def get_all_notification(request):
    notificationService = NotificationService()
    return notificationService.get_all_notification(request)

@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def create_notification(request):
    notificationService = NotificationService()
    return notificationService.create_notification(request)

@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def update_seem_notification(request):
    notificationService = NotificationService()
    return notificationService.update_seem_notification(request)