from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.middleware.csrf import get_token
from django.middleware import csrf
from django.conf import settings
from rest_framework.decorators import api_view,action,permission_classes,authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from user.api.authenticate import CustomAuthentication
from user.models import User
from chat.models import Chat , Conversation , GroupChat , Member
from chat.models import Notification
from django.db.models import Q
from .serializers import ConversationSerializer , ChatSerialzier , NotificationSerializer
from .serializers import GroupSerializer , MemberSerializer , ConversationGroupSerializer
import uuid
import json
import base64
import uuid 
import os
import ast

# ---------------------------------------------------------------------------- #
#                                 CONVERSATION                                 #
# ---------------------------------------------------------------------------- #
@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def create_conversation(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    
    def createConvasertion(userTo , userCurrent , contentLast):
        conversation = Conversation.objects.filter( 
            Q(user_from = userCurrent , user_to = userTo)
            | Q(user_from = userTo, user_to = userCurrent)
        )
        if len(conversation) > 0:
            serializer = ConversationSerializer(conversation[0] , many = False)
            response.data = {
                "success" : True ,
                "is_create" : True ,
                "conversation" : serializer.data,
                "status" : status.HTTP_200_OK
            }
            response.status_code = status.HTTP_200_OK
            return response
        notification = [
            { 
                userCurrent.email : 0
            },
            {
                userTo.email : 0
            }
        ]
        conversation = Conversation.objects.create(
            user_from = userCurrent ,
            user_to = userTo ,
            content_last = contentLast,
            list_message_sent = notification ,
            list_user_seen = [userCurrent.email]
        )
        conversation.save()
        chatCurrent = Chat.objects.create(
          user_id = userCurrent ,
          conversation_id = conversation  ,
          content = contentLast ,
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

    try:
        data_request= json.loads(request.body.decode('utf-8'))
        userTo =User.objects.get( email = data_request['user_to'])
        userCurrent = request.user
        contentLast =data_request['content_last']
        try:
            return createConvasertion(userTo , userCurrent ,contentLast )
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
        return notFound()

@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def chat_conversation(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    def onConversation(conversation_id , userCurrent , contentLast):
        conversation = Conversation.objects.get( 
            id = conversation_id
        )
        conversation.content_last = contentLast
        if conversation.group_id == None:
            print(conversation.list_message_sent)
            list_message_sent = json.loads(str(conversation.list_message_sent))
            print(list_message_sent)
            listMessageSent = []
            for message_sent in list_message_sent:
                print(message_sent, type(message_sent))
                message_sent_dict = ast.literal_eval(message_sent)
                print('message_sent_dict.keys())[0]', message_sent_dict)
                if next(iter(message_sent_dict)) != userCurrent.email:
                    userSent = {
                        next(iter(message_sent_dict)): message_sent_dict[next(iter(message_sent_dict))] + 1
                    }
                    listMessageSent.append(userSent)
                else:
                    listMessageSent.append(message_sent_dict)
            conversation.list_message_sent = listMessageSent
        conversation.list_user_seen = [userCurrent.email]
        conversation.save()
        chatCurrent = Chat.objects.create(
          user_id = userCurrent ,
          conversation_id = conversation  ,
          content = contentLast ,
        )

        chatCurrent.save()

        response.data = {
            "success" : True ,
            "is_create" : False ,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response

    try:
        data_request= json.loads(request.body.decode('utf-8'))
        userCurrent = request.user
        conversation_id = data_request['conversation_id']
        contentLast =data_request['content_last']
        try:
            return onConversation(conversation_id , userCurrent , contentLast)
        except Exception as e:
            print(e)
            return notFound()
    except Exception as e:
        print(e)
        return notFound()

@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def seem_conversation(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    def checkUserSeem(email_user , list_user_seem) -> bool:
        for email in list_user_seem:
            if email == email_user:
                return True
        return False
    def seemConversation(conversation_id , userCurrent):
        conversation = Conversation.objects.get( 
            id = conversation_id
        )
        list_message_sent = json.loads(str(conversation.list_message_sent))
        listMessageSent = []
        for message_sent in list_message_sent:
            message_sent_dict = ast.literal_eval(message_sent)
            if next(iter(message_sent_dict)) != userCurrent.email:
                userSent = {
                    next(iter(message_sent_dict)): message_sent_dict[next(iter(message_sent_dict))]
                }
                listMessageSent.append(userSent)
            else:
                print( 'seem ' ,next(iter(message_sent_dict)), userCurrent.email )
                userSent = {
                    next(iter(message_sent_dict)): 0
                }
                listMessageSent.append(userSent)
        conversation.list_message_sent = listMessageSent
        list_user_seen = conversation.list_user_seen
        if checkUserSeem( userCurrent.email ,list_user_seen) == False:
            list_user_seen.append(userCurrent.email)
            conversation.list_user_seen = list_user_seen
        conversation.save()
            
        response.data = {
            "success" : True ,
            "is_create" : False ,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response

    try:
        data_request= json.loads(request.body.decode('utf-8'))
        userCurrent = request.user
        conversation_id = data_request['conversation_id']
        try:
            return seemConversation(conversation_id , userCurrent)
        except Exception as e:
            print(e)
            return notFound()
    except Exception as e:
        print(e)
        return notFound()
    
@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def get_conversation(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    
    def getConvasertion(userCurrent):
        conversations = Conversation.objects.filter(
            Q(user_from = userCurrent ) | Q(user_to = userCurrent)
        )
        serializer = ConversationSerializer(conversations , many = True)
        response.data = {
            "success" : True ,
            "conversation" : serializer.data,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response

    try:
        userCurrent = request.user
        return getConvasertion(userCurrent)
    except Exception as e:
        print(e)
        return notFound()

@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def get_all_conversation(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    
    def getConvasertion(userCurrent):
        conversations = Conversation.objects.filter(
           Q( user_from = userCurrent , group_id__isnull = True ) 
           | Q( user_to = userCurrent , group_id__isnull = True)
        )
        serializer = ConversationSerializer(conversations , many = True)
        response.data = {
            "success" : True ,
            "conversation" : serializer.data,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response

    try:
        userCurrent = request.user
        return getConvasertion(userCurrent)
    except Exception as e:
        print(e)
        return notFound()


@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def get_conversation(request , uuid):
    response = Response()
    print("User:", request.user)
    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    
    def getConvasertion(userCurrent):
        conversation = Conversation.objects.get(
           Q(id = uuid)
        )
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

    try:
        userCurrent = request.user
        return getConvasertion(userCurrent)
    except Exception as e:
        print(e)
        return notFound()

@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def checked_conversation(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    def checkConversation(userTo , userCurrent ):
        try:
            conversation = Conversation.objects.get( 
                Q(user_from = userCurrent , user_to = userTo)
                | Q(user_from = userTo, user_to = userCurrent)
            )
            chats = Chat.objects.filter(conversation_id = conversation)
            serializer = ChatSerialzier(chats , many = True)
            response.data = {
                "empty" : False ,
                "conversation_id": str(conversation.id) ,
                "chats" : serializer.data,
                "status" : status.HTTP_200_OK
            } 
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as e:
            print(e)
            response.data = {
                "empty" : True ,
                "status" : status.HTTP_200_OK
            } 
            response.status_code = status.HTTP_200_OK
            return response


    try:
        data_request= json.loads(request.body.decode('utf-8'))
        userTo =User.objects.get( email = data_request['user_to'])
        userCurrent = request.user
        
        return checkConversation(userTo , userCurrent)
    
    except Exception as e:
        print(e)
        return notFound()
    

# ---------------------------------------------------------------------------- #
#                                  GROUP CHAT                                  #
# ---------------------------------------------------------------------------- #

@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def chat_group(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    def onConversation(conversation_id , userCurrent , contentLast):
        conversation = Conversation.objects.get( id = conversation_id)
        conversation.content_last = contentLast

        if conversation.group_id != None:
            list_message_sent = json.loads(str(conversation.list_message_sent))
            listMessageSent = []
            for message_sent in list_message_sent:
                message_sent_dict = ast.literal_eval(message_sent)
                if next(iter(message_sent_dict)) != userCurrent.email:
                    userSent = {
                        next(iter(message_sent_dict)): message_sent_dict[next(iter(message_sent_dict))] + 1
                    }
                    listMessageSent.append(userSent)
                else:
                    listMessageSent.append(message_sent_dict)
            conversation.list_message_sent = listMessageSent
        conversation.list_user_seen = [userCurrent.email]
        conversation.save()

        chatCurrent = Chat.objects.create(
          user_id = userCurrent ,
          conversation_id = conversation  ,
          content = contentLast ,
        )

        chatCurrent.save()

        response.data = {
            "success" : True ,
            "is_create" : False ,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response

    try:
        data_request= json.loads(request.body.decode('utf-8'))
        userCurrent = request.user
        conversation_id = data_request['conversation_id']
        contentLast =data_request['content_last']
        
        return onConversation( conversation_id , userCurrent , contentLast)

    except Exception as e:
        print(e)
        return notFound()
    
@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def create_group(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
    def createGroup(userCurrent,listMember , name , description) :
        groupChat = GroupChat.objects.create(
            name = name , description = description
        )
        notification = [
            {
                userCurrent.email : 0
            }
        ]
        try:
            Member.objects.create(
                is_manager = True ,
                user_id = userCurrent ,
                group_id = groupChat
            )
        except Exception as e:
            print("ERROR MEMBER ADMIN")
            groupChat.delete()
            return notFound()
        listMemberNew = []
        for i in listMember:
            print(i)
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
                        userMember.email : 0
                    }
                )
            except:
                pass
        try:
            conversation = Conversation.objects.create(
                user_from = userCurrent ,
                group_id = groupChat ,
                list_message_sent = notification ,
                list_user_seen = [userCurrent.email]
            )
        except Exception as e:
            groupChat.delete()
            for i in listMemberNew:
                i.delete()
            print("ERROR Create conversation")
            return notFound()

        serializer = ConversationGroupSerializer(conversation , many = False)
        response.data = {
            "success" : True ,
            "is_create" : True ,
            "conversation" : serializer.data,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response

    try:
        data_request= json.loads(request.body.decode('utf-8'))
        userCurrent = request.user
        name = data_request['name']
        description =  data_request['description']
        listMember = data_request['list_member']
        return createGroup(userCurrent,listMember , name , description) 
    except Exception as e:
        print(e)
        return notFound()

@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def get_all_group_user(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
    def getAllGroup(userCurrent) :
        groupChat = GroupChat.objects.filter(
            member_group__user_id=userCurrent
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

    try:
        userCurrent = request.user
        return getAllGroup(userCurrent) 
    except Exception as e:
        print(e)
        return notFound()

# ---------------------------------------------------------------------------- #
#                                 NOTIFICATION                                 #
# ---------------------------------------------------------------------------- #

@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def get_all_notification(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
    def getAllNotification(userCurrent) :
        notifications = Notification.objects.filter(user_id = userCurrent).order_by('-created_at')
        serializer = NotificationSerializer(notifications , many = True)
        response.data = {
            "success" : True ,
            "notifications" : serializer.data,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response

    try:
        userCurrent = request.user
        return getAllNotification(userCurrent) 
    except Exception as e:
        print(e)
        return notFound()

@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def create_notification(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
    def createNotification(
            userCurrent , content ,
            email_user_chat ,
            type , conversation_id
        ):
        conversation = Conversation.objects.get(id = conversation_id)
        if conversation.group_id == None:

            if userCurrent != conversation.user_from:
                notificationUserFrom = Notification.objects.create(
                    user_id = conversation.user_from , content = content ,
                    conversation_id = conversation , email_user_chat = email_user_chat ,
                    type = type , is_seem = False
                )
            else:
                notificationUserTo = Notification.objects.create(
                    user_id = conversation.user_to , content = content ,
                    conversation_id = conversation , email_user_chat = email_user_chat ,
                    type = type , is_seem = False
                )
        else:
            memberNotifications = Member.objects.filter(group_id = conversation.group_id)
            for member in memberNotifications:
                notificationMember = Notification.objects.create(
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

    try:
        data_request= json.loads(request.body.decode('utf-8'))
        userCurrent = request.user
        content = data_request['content']
        email_user_chat = data_request['email_user_chat']
        conversation_id = data_request['conversation_id']
        type = data_request['type']
        return createNotification(
            userCurrent , content ,
            email_user_chat ,
            type , conversation_id
        ) 
    except Exception as e:
        print(e)
        return notFound()

@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def update_seem_notification(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
    def createNotification(
            userCurrent , notification_id 
        ):
        notification = Notification.objects.get( id = notification_id)
        notification.is_seem = True
        notification.save()
        response.data = {
            "success" : True ,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response

    try:
        data_request= json.loads(request.body.decode('utf-8'))
        userCurrent = request.user
        notification_id = data_request['notification_id']
        return createNotification(
            userCurrent , notification_id ,
        ) 
    except Exception as e:
        print(e)
        return notFound()