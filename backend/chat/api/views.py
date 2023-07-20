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
from chat.models import Chat , Conversation
from django.db.models import Q
from .serializers import ConversationSerializer , ChatSerialzier
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
@permission_classes([])
@authentication_classes([JWTAuthentication])
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
        conversation = Conversation.objects.get( Q(user_from = userCurrent , user_to = userTo) | Q(user_from = userTo, user_to = userCurrent))
        conversation.content_last = contentLast
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
@permission_classes([])
@authentication_classes([JWTAuthentication])
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
            user_from = userCurrent 
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
@permission_classes([])
@authentication_classes([JWTAuthentication])
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
           Q( user_from = userCurrent ) | Q( user_to = userCurrent)
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
@permission_classes([])
@authentication_classes([JWTAuthentication])
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
        print(conversation.content_last  )
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
        return getConvasertion(userCurrent)
    except Exception as e:
        print(e)
        return notFound()