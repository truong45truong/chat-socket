from rest_framework.decorators import api_view
from ..services.service_chat import ChatService
from ..services.service_notification import NotificationService
from ..services.service_group import GroupService


# ---------------------------------------------------------------------------- #
#                                 CONVERSATION                                 #
# ---------------------------------------------------------------------------- #
@api_view(['POST'])
def create_conversation(request):
    chatService = ChatService()
    return chatService.create_conversation(request)

@api_view(['GET'])
def get_all_conversation(request):
    chatService = ChatService()
    return chatService.get_all_conversation(request)
@api_view(['GET'])
def get_conversation(request , uuid):
    chatService = ChatService()
    return chatService.get_conversation(request,uuid)

@api_view(['POST'])
def chat_conversation(request):
    chatService = ChatService()
    return chatService.chat_conversation(request)

@api_view(['POST'])
def seem_conversation(request):
    chatService = ChatService()
    return chatService.seem_conversation(request)

@api_view(['POST'])
def checked_conversation(request):
    chatService = ChatService()
    return chatService.check_conversation(request)

# ---------------------------------------------------------------------------- #
#                                  GROUP CHAT                                  #
# ---------------------------------------------------------------------------- #

@api_view(['POST'])
def chat_group(request):
    groupService = GroupService()
    return groupService.chat_group(request)

@api_view(['POST'])
def create_group(request):
    groupService = GroupService()
    return groupService.create_group(request)

@api_view(['GET'])
def get_all_group_user(request):
    groupService = GroupService()
    return groupService.get_all_group_user(request)

# ---------------------------------------------------------------------------- #
#                                 NOTIFICATION                                 #
# ---------------------------------------------------------------------------- #

@api_view(['GET'])
def get_all_notification(request):
    notificationService = NotificationService()
    return notificationService.get_all_notification(request)

@api_view(['POST'])
def create_notification(request):
    notificationService = NotificationService()
    return notificationService.create_notification(request)

@api_view(['POST'])
def update_seem_notification(request):
    notificationService = NotificationService()
    return notificationService.update_seem_notification(request)