from chat_base.core.constants import message_code
from chat_base.core.ultis.exceptions import CustomAPIException
from rest_framework import status
from rest_framework.response import Response
from chat_user.chat.models import Notification , Conversation , Member
from ..serializers.serializer_notification import NotificationSerializer
from ..serializers.serializer_notification import NotificationValidSerializer
import json
class NotificationService:

    def __init__(self):
        super(NotificationService,self).__init__()

    def get_all_notification(self , req_data) -> Response:
        response = Response()
        user_current = req_data.user
        notifications = Notification.objects.filter(user_id = user_current).order_by('-created_at')
        serializer = NotificationSerializer(notifications , many = True)
        response.data = {
            "success" : True ,
            "notifications" : serializer.data,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    
    def create_notification(self , req_data) -> Response:
        response = Response()
        user_current  = req_data.user

        try:
            data_request= json.loads(req_data.body.decode('utf-8'))
        except:
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
        
        serialzier_valid = NotificationValidSerializer(data = data_request)
        serialzier_valid.is_valid(raise_exception= True)
        content = serialzier_valid.data.get('content')
        email_user_chat = serialzier_valid.data.get('email_user_chat')
        conversation = serialzier_valid.data.get('conversation_id')
        type = serialzier_valid.data.get('type')
        if conversation.group_id == None:

            if user_current != conversation.user_from:
                Notification.objects.create(
                    user_id = conversation.user_from , content = content ,
                    conversation_id = conversation , email_user_chat = email_user_chat ,
                    type = type , is_seem = False
                )
            else:
                Notification.objects.create(
                    user_id = conversation.user_to , content = content ,
                    conversation_id = conversation , email_user_chat = email_user_chat ,
                    type = type , is_seem = False
                )
        else:
            memberNotifications = Member.objects.filter(group_id = conversation.group_id)
            for member in memberNotifications:
                Notification.objects.create(
                    user_id = member.user_id , content = content ,
                    conversation_id = conversation , email_user_chat = email_user_chat ,
                    type = type , is_seem = False
                )
        

        response.data = {
            "success" : True ,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    
    def update_seem_notification(self , req_data) -> Response:
        response = Response()
        try:
            data_request= json.loads(req_data.body.decode('utf-8'))
            notification_id = data_request['notification_id']
            notification = Notification.objects.get( id = notification_id)
        except:
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
        
        notification.is_seem = True
        notification.save()
        response.data = {
            "success" : True ,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response