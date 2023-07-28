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

path_upload_image = str(settings.BASE_DIR)+"/media/photos"
path_upload_video = str(settings.BASE_DIR)+"/media/videos"
# ---------------------------------------------------------------------------- #
#                                  LOGIN USER                                  #
# ---------------------------------------------------------------------------- #
@api_view(['POST'])
def create_conversation(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error Auth" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    def onConversation(userTo , userCurrent , contentLast):
        conversation = Conversation.objects.get( 
            Q(user_from = userCurrent , user_to = userTo)
            | Q(user_from = userTo, user_to = userCurrent)
        )
        conversation.content_last = contentLast
        print('conversation' , conversation.user_from , conversation.user_to)
        if conversation.user_from != userCurrent:
            conversation.is_sent = False
        else:
            conversation.is_sent = True
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
    
    def createConvasertion(userTo , userCurrent , contentLast):
        conversation = Conversation.objects.create(
            user_from = userCurrent ,
            user_to = userTo ,
            content_last = contentLast,
            is_sent = True,
            is_seen = False
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
        jwtToken = request.COOKIES.get('refresh_token')
        refresh_token = RefreshToken(jwtToken)
        decoded_token = refresh_token.payload
        userTo =User.objects.get( email = data_request['user_to'])
        userCurrent = User.objects.get(id = decoded_token['user_id'])
        contentLast =data_request['content_last']
        try:
            return onConversation(userTo , userCurrent , contentLast)
        except Exception as e:
            print(e)
            return createConvasertion(userTo , userCurrent , contentLast) 
    except Exception as e:
        print(e)
        return notFound()

@api_view(['POST'])
def create_conversation(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error Auth" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    def onConversation(userTo , userCurrent , contentLast):
        conversation = Conversation.objects.get( 
            Q(user_from = userCurrent , user_to = userTo)
            | Q(user_from = userTo, user_to = userCurrent)
        )
        conversation.content_last = contentLast
        print('conversation' , conversation.user_from , conversation.user_to)
        if conversation.user_from != userCurrent:
            conversation.is_sent = False
        else:
            conversation.is_sent = True
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
    
    def createConvasertion(userTo , userCurrent , contentLast):
        conversation = Conversation.objects.create(
            user_from = userCurrent ,
            user_to = userTo ,
            content_last = contentLast,
            is_sent = True,
            is_seen = False
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
        jwtToken = request.COOKIES.get('refresh_token')
        refresh_token = RefreshToken(jwtToken)
        decoded_token = refresh_token.payload
        userTo =User.objects.get( email = data_request['user_to'])
        userCurrent = User.objects.get(id = decoded_token['user_id'])
        contentLast =data_request['content_last']
        try:
            return onConversation(userTo , userCurrent , contentLast)
        except Exception as e:
            print(e)
            return createConvasertion(userTo , userCurrent , contentLast) 
    except Exception as e:
        print(e)
        return notFound()
    
@api_view(['GET'])
def get_conversation(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error Auth" , 'value' : "Failed"
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
        jwtToken = request.COOKIES.get('refresh_token')
        refresh_token = RefreshToken(jwtToken)
        decoded_token = refresh_token.payload
        userCurrent = User.objects.get(id = decoded_token['user_id'])
        return getConvasertion(userCurrent)
    except Exception as e:
        print(e)
        return notFound()

@api_view(['GET'])
def get_all_conversation(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error Auth" , 'value' : "Failed"
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
        jwtToken = request.COOKIES.get('refresh_token')
        refresh_token = RefreshToken(jwtToken)
        decoded_token = refresh_token.payload
        userCurrent = User.objects.get(id = decoded_token['user_id'])
        return getConvasertion(userCurrent)
    except Exception as e:
        print(e)
        return notFound()

@api_view(['GET'])
def get_conversation(request , uuid):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error Auth" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    
    def getConvasertion(userCurrent):
        conversation = Conversation.objects.get(
           Q(id = uuid)
        )
        chats = Chat.objects.filter(conversation_id = conversation)

        serializer = ChatSerialzier(chats , many = True)
        response.data = {
            "success" : True ,
            "chats" : serializer.data,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response

    try:
        jwtToken = request.COOKIES.get('refresh_token')
        refresh_token = RefreshToken(jwtToken)
        decoded_token = refresh_token.payload
        userCurrent = User.objects.get(id = decoded_token['user_id'])
        print("start get conversation")
        return getConvasertion(userCurrent)
    except Exception as e:
        print(e)
        return notFound()

@api_view(['POST'])
def checked_conversation(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error Auth" , 'value' : "Failed"
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
        jwtToken = request.COOKIES.get('refresh_token')
        refresh_token = RefreshToken(jwtToken)
        decoded_token = refresh_token.payload
        userTo =User.objects.get( email = data_request['user_to'])
        userCurrent = User.objects.get(id = decoded_token['user_id'])
        
        return checkConversation(userTo , userCurrent)
    
    except Exception as e:
        print(e)
        return notFound()
    

# ---------------------------------------------------------------------------- #
#                                  GROUP CHAT                                  #
# ---------------------------------------------------------------------------- #

@api_view(['POST'])
def chat_group(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error Auth" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    def onConversation(conversation_id , userCurrent , contentLast):
        conversation = Conversation.objects.get( id = conversation_id)
        conversation.content_last = contentLast

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
        jwtToken = request.COOKIES.get('refresh_token')
        refresh_token = RefreshToken(jwtToken)
        decoded_token = refresh_token.payload
        userCurrent = User.objects.get(id = decoded_token['user_id'])
        conversation_id = data_request['conversation_id']
        contentLast =data_request['content_last']
        
        return onConversation( conversation_id , userCurrent , contentLast)

    except Exception as e:
        print(e)
        return notFound()
    
@api_view(['POST'])
def create_group(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error Auth" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
    def createGroup(userCurrent,listMember , name , description) :
        groupChat = GroupChat.objects.create(
            name = name , description = description
        )
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
            except:
                pass
        try:
            conversation = Conversation.objects.create(
                user_from = userCurrent ,
                group_id = groupChat ,
                is_sent = True,
                is_seen = False
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
        jwtToken = request.COOKIES.get('refresh_token')
        refresh_token = RefreshToken(jwtToken)
        decoded_token = refresh_token.payload
        userCurrent = User.objects.get(id = decoded_token['user_id'])
        name = data_request['name']
        description =  data_request['description']
        listMember = data_request['list_member']
        print(listMember)
        for i in listMember:
            print(i)
        return createGroup(userCurrent,listMember , name , description) 
    except Exception as e:
        print(e)
        return notFound()

@api_view(['GET'])
def get_all_group_user(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error Auth" , 'value' : "Failed"
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
        jwtToken = request.COOKIES.get('refresh_token')
        refresh_token = RefreshToken(jwtToken)
        decoded_token = refresh_token.payload
        userCurrent = User.objects.get(id = decoded_token['user_id'])
        return getAllGroup(userCurrent) 
    except Exception as e:
        print(e)
        return notFound()

# ---------------------------------------------------------------------------- #
#                                 NOTIFICATION                                 #
# ---------------------------------------------------------------------------- #

@api_view(['GET'])
def get_all_notification(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error Auth" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
    def getAllNotification(userCurrent) :
        notifications = Notification.objects.filter(user_id = userCurrent)
        serializer = NotificationSerializer(notifications , many = True)
        response.data = {
            "success" : True ,
            "notifications" : serializer.data,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response

    try:
        jwtToken = request.COOKIES.get('refresh_token')
        refresh_token = RefreshToken(jwtToken)
        decoded_token = refresh_token.payload
        userCurrent = User.objects.get(id = decoded_token['user_id'])
        return getAllNotification(userCurrent) 
    except Exception as e:
        print(e)
        return notFound()

@api_view(['POST'])
def create_notification(request):
    response = Response()

    def notFound():
        response.data = {
            "success" : False , 'error' : {
                'type' : "Error Auth" , 'value' : "Failed"
            } , 
            'status' : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
    def createNotification(
            userCurrent , content ,
            group_id , email_user_chat ,
            type 
        ):
        notification = Notification.objects.create(
            user_id = userCurrent , content = content ,
            group_id = group_id , email_user_chat = email_user_chat ,
            type = type
        )

        response.data = {
            "success" : True ,
            "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response

    try:
        data_request= json.loads(request.body.decode('utf-8'))
        jwtToken = request.COOKIES.get('refresh_token')
        refresh_token = RefreshToken(jwtToken)
        decoded_token = refresh_token.payload
        userCurrent = User.objects.get(id = decoded_token['user_id'])
        content = data_request['content']
        group_id = data_request['group_id']
        email_user_chat = data_request['email_user_chat']
        type = data_request['type']
        return createNotification(
            userCurrent , content ,
            group_id , email_user_chat ,
            type 
        ) 
    except Exception as e:
        print(e)
        return notFound()