from chat_base.core.constants import message_code
from chat_base.core.ultis.exceptions import CustomAPIException
from chat_user.chat.models import Conversation , Chat , GroupChat , Member
from chat_user.user.models import User
from ..serializers.serializer_chat import ConversationValidSerializer
from ..serializers.serializer_chat import ConversationSerializer
from ..serializers.serializer_chat import ChatConversationValidSerializer
from ..serializers.serializer_chat import ChatSerialzier
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
import json
import ast

class ChatService:

    def __init__(self):
        super(ChatService,self).__init__()
    
    def check_user_seem(self , email_user , list_user_seem) -> bool:
        for email in list_user_seem:
            if email == email_user:
                return True
        return False
    
    def create_conversation(self,req_data) -> Response:
        response = Response()
        user_current  = req_data.user

        try:
            data_request= json.loads(req_data.body.decode('utf-8'))
            data_request['user_from'] = user_current.email
        except:
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
        
        
        serializer_valid = ConversationValidSerializer(data=data_request)
        serializer_valid.is_valid(raise_exception=True)
        user_to  = serializer_valid.data.get('obj_user_to')
        content_last = serializer_valid.data.get('content_last')
        notification = [
            { 
                user_current.email : 0
            },
            {
                user_to.email : 1
            }
        ]
        conversation = Conversation.objects.create(
            user_from = user_current ,
            user_to = user_to ,
            content_last = content_last,
            list_message_sent = notification ,
            list_user_seen = [user_current.email] ,
            user_chat = user_current.email,
        )
        conversation.save()
        chatCurrent = Chat.objects.create(
          user_id = user_current ,
          conversation_id = conversation  ,
          content = content_last ,
        )

        chatCurrent.save()
        serializer = ConversationSerializer(conversation , many = False)
        response.data = {
            "success" : True ,
            "is_create" : True ,
            "conversation" : serializer.data,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    
    def chat_conversation(self,req_data) -> Response:
        response = Response()
        user_current  = req_data.user

        try:
            data_request= json.loads(req_data.body.decode('utf-8'))
            data_request['user_from'] = user_current.email
            print('req_data.body' , req_data.body, type(req_data.body) )
            print('req_data' , req_data.POST)
        except:
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
        
        serializer_valid = ChatConversationValidSerializer(data=data_request)
        serializer_valid.is_valid(raise_exception=True)
        content_last = serializer_valid.data.get('content_last')
        conversation = serializer_valid.data.get('obj_conversation')
        conversation.content_last = content_last
        conversation.user_chat = user_current.email
        if conversation.group_id == None:
            list_message_sent = json.loads(str(conversation.list_message_sent))
            listMessageSent = []
            for message_sent in list_message_sent:
                message_sent_dict = ast.literal_eval(message_sent)
                if next(iter(message_sent_dict)) != user_current.email:
                    userSent = {
                        next(iter(message_sent_dict)): message_sent_dict[next(iter(message_sent_dict))] + 1
                    }
                    listMessageSent.append(userSent)
                else:
                    listMessageSent.append(message_sent_dict)
            conversation.list_message_sent = listMessageSent
        conversation.list_user_seen = [user_current.email]
        conversation.save()
        chatCurrent = Chat.objects.create(
          user_id = user_current ,
          conversation_id = conversation  ,
          content = content_last ,
        )

        chatCurrent.save()

        response.data = {
            "success" : True ,
            "is_create" : False ,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    
    def seem_conversation(self, req_data) -> Response:
        response = Response()
        user_current  = req_data.user

        try:
            data_request= json.loads(req_data.body.decode('utf-8'))
            data_request['user_from'] = user_current.email
            conversation = Conversation.objects.get( 
            id = data_request['conversation_id']
        )
        except:
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
    
        list_message_sent = json.loads(str(conversation.list_message_sent))
        listMessageSent = []
        for message_sent in list_message_sent:
            message_sent_dict = ast.literal_eval(message_sent)
            if next(iter(message_sent_dict)) != user_current.email:
                userSent = {
                    next(iter(message_sent_dict)): message_sent_dict[next(iter(message_sent_dict))]
                }
                listMessageSent.append(userSent)
            else:
                userSent = {
                    next(iter(message_sent_dict)): 0
                }
                listMessageSent.append(userSent)
        conversation.list_message_sent = listMessageSent
        list_user_seen = conversation.list_user_seen
        if self.check_user_seem( user_current.email ,list_user_seen) == False:
            list_user_seen.append(user_current.email)
            conversation.list_user_seen = list_user_seen
        conversation.save()
            
        response.data = {
            "success" : True ,
            "is_create" : False ,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    
    def get_all_conversation(self, req_data) -> Response:
        user_current = req_data.user
        response = Response()
        conversations = Conversation.objects.filter(
           Q( user_from = user_current , group_id__isnull = True ) 
           | Q( user_to = user_current , group_id__isnull = True)
        )
        serializer = ConversationSerializer(conversations , many = True)
        response.data = {
            "success" : True ,
            "conversation" : serializer.data,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    
    def get_conversation(self, req_data , uuid):
        response = Response()
        try:
            conversation = Conversation.objects.get( 
                Q(id = uuid)
            )
        except:
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
        
        conversation.save()
        chats = Chat.objects.filter(conversation_id = conversation)[:99]

        serializer = ChatSerialzier(chats , many = True)
        response.data = {
            "success" : True ,
            "chats" : serializer.data,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    def check_conversation(self,req_data) -> Response:
        response = Response()
        user_current  = req_data.user

        try:
            data_request= json.loads(req_data.body.decode('utf-8'))
            user_to = data_request['user_to']
        except:
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
        
        conversation = Conversation.objects.filter( 
            Q(user_from = user_current , user_to__email = user_to)
            | Q(user_from__email = user_to, user_to = user_current)
        )
        if len(conversation) == 0:
            response.data = {
                "empty" : True ,
                "status" : status.HTTP_200_OK
            } 
        else:
            chats = Chat.objects.filter(conversation_id = conversation[0])
            serializer = ChatSerialzier(chats , many = True)
            response.data = {
                "empty" : False ,
                "conversation_id": str(conversation.id) ,
                "chats" : serializer.data,
                "status" : status.HTTP_200_OK
            } 
        response.status_code = status.HTTP_200_OK
        return response
    
    
    