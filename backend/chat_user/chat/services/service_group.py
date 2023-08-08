from chat_base.core.constants import message_code
from chat_base.core.ultis.exceptions import CustomAPIException
from chat_user.chat.models import Conversation , Chat , GroupChat , Member
from chat_user.user.models import User
from ..serializers.serializer_group import ChatGroupValidSerializer
from ..serializers.serializer_group import GroupValidSerializer
from ..serializers.serializer_group import ConversationGroupSerializer
from rest_framework import status
from rest_framework.response import Response
import json
import ast

class GroupService:

    def __init__(self):
        super(GroupService,self).__init__()

    def check_user_seem(self , email_user , list_user_seem) -> bool:
        for email in list_user_seem:
            if email == email_user:
                return True
        return False

    def chat_group(self , req_data):
        response = Response()
        user_current  = req_data.user
        try:
            data_request= json.loads(req_data.body.decode('utf-8'))
            data_request['user_from'] = user_current.email
        except:
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
        
        serializer_valid = ChatGroupValidSerializer(data= data_request)
        serializer_valid.is_valid(raise_exception= True)
        conversation = serializer_valid.data.get('obj_conversation')
        conversation.content_last = serializer_valid.data.get('content_last')
        conversation.user_chat = user_current.email

        if conversation.group_id != None:
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
          content = serializer_valid.data.get('content_last') ,
        )

        chatCurrent.save()

        response.data = {
            "success" : True ,
            "is_create" : False ,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    
    def create_group(self , req_data):
        response = Response()
        user_current  = req_data.user
        try:
            data_request= json.loads(req_data.body.decode('utf-8'))
            data_request['user_from'] = user_current.email
            
        except:
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
        
        serializer_valid = GroupValidSerializer(data = data_request)
        serializer_valid.is_valid(raise_exception=True)
        name_group = serializer_valid.data.get('name')
        description_group = serializer_valid.data.get('description')
        list_member = serializer_valid.data.get('list_member')
        groupChat = GroupChat.objects.create(
            name = name_group , description = description_group
        )
        notification = [
            {
                user_current.email : 0
            }
        ]
        try:
            Member.objects.create(
                is_manager = True ,
                user_id = user_current ,
                group_id = groupChat
            )
        except Exception as e:
            groupChat.delete()
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
        listMemberNew = []
        for i in list_member:

            try:
                userMember = User.objects.get(email = i)
                member = Member.objects.create(
                    is_manager = False ,
                    user_id = userMember ,
                    group_id = groupChat
                )
                listMemberNew.append(member)
                notification.append(
                    {
                        userMember.email : 1
                    }
                )
            except:
                pass
        try:
            conversation = Conversation.objects.create(
                user_from = user_current ,
                group_id = groupChat ,
                list_message_sent = notification ,
                list_user_seen = [user_current.email] ,
                content_last = "created group new" ,
                user_chat = user_current.email
            )
        except Exception as e:
            groupChat.delete()
            for i in listMemberNew:
                i.delete()
            raise CustomAPIException(detail=message_code.INVALID_INPUT)

        serializer = ConversationGroupSerializer(conversation , many = False)
        response.data = {
            "success" : True ,
            "is_create" : True ,
            "conversation" : serializer.data,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    
    def get_all_group_user(self,req_data):
        response = Response()
        user_current = req_data.user
        groupChat = GroupChat.objects.filter(
            members_groups__user_id=user_current
        )
        group_ids = list(groupChat.values_list('id', flat=True))
        conversation = Conversation.objects.filter(group_id_id__in=group_ids )
        serializer = ConversationGroupSerializer(conversation , many = True)
        response.data = {
            "success" : True ,
            "groups" : serializer.data,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    
    