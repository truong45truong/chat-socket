from chat_base.auth.services import AuthService
from chat_user.user.models import User , Membership
from chat_base.core.constants import message_code
from chat_base.core.ultis.exceptions import CustomAPIException
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from ..serializers.serializers import UserSerializer , RegisterSerializer
from ..serializers.serializers import MemberShipSerializer
from django.conf import settings
import json

class UserService(AuthService):
    def __init__(self):
        super(UserService , self).__init__()
    
    def get_user(self,email):
        user_model = User
        try:
            user = user_model.objects.get(email = email)
            return user
        except user_model.DoesNotExist:
            raise CustomAPIException(detail=message_code.THIS_EMAIL_NOT_YET_REGISTER)
    def login(self,req_data):
        response = Response()
        try:
            data_request= json.loads(req_data.body.decode('utf-8'))
            username = data_request['username']
            password = data_request['password']
        except:
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
        #check username
        try:
            user = authenticate(username=username, password=password)
        except Exception as e:
            users_l = User.objects.all()
            for i in users_l:
                print(i)
            print(e)
            raise CustomAPIException(detail=message_code.USERNAME_OR_PASSWORD_IS_INCORRECT)
        if user is not None:
            if user.is_active:
                queryset = User.objects.get(username = username)
                tokens = self.get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                    value=tokens["refresh"],
                    expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                serializer = UserSerializer(queryset,many = False)
                response.data = {
                    "success" : "login success" , "access_token" : tokens["access"] ,
                    "user" : serializer.data ,'status' : status.HTTP_200_OK
                }
                response.status_code = status.HTTP_200_OK
                return response
        raise CustomAPIException(detail=message_code.USERNAME_OR_PASSWORD_IS_INCORRECT)
    def register(self,req_data):
        response = Response()
        try:
            data_request= json.loads(req_data.body.decode('utf-8'))
        except:
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
        serializer = RegisterSerializer(data=data_request)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        name = serializer.data.get('name')
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = User.objects.create(
            username=username,photo = None ,
            name = name , email = email
        )
        user.password  = make_password(password)
        user.save()
        tokens = self.get_tokens_for_user(user)
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=tokens["refresh"],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=None
        )
        serializer = UserSerializer(user,many = False)
        response.data = {
            "success" : "register success" , "access_token" : tokens["access"] ,
            "user" : serializer.data ,'status' : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    def search_user(self,req_data):
        response = Response()
        user_current = req_data.user
        try:
            key_search = req_data.GET.get('key_search')
        except:
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
        userSearches = User.objects.filter(
            email__icontains=key_search
        ).exclude(
            email= user_current.email
        )[:5]
        serializer = UserSerializer(userSearches,many = True)

        response.data = {
            "users" : serializer.data,
            "success" : True ,
            "status"  : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    def add_member_ship(self,req_data):
        response = Response()
        user_current = req_data.user
        try:
            data_request= json.loads(req_data.body.decode('utf-8'))
            user_added = data_request['user_to']
            userAdded = User.objects.get(email=user_added)
        except:
            raise CustomAPIException(detail=message_code.INVALID_INPUT)
        checkMember = Membership.objects.filter(from_user = user_current , to_user = userAdded)
        if len(checkMember) > 0:
            checkMember[0].delete()
        else:
            Membership.objects.create(
                from_user = user_current , 
                to_user = userAdded,
            )

        response.data = {
            "success" : True ,
            "status"  : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    def get_all_member_ship(self,req_data):
        response = Response()
        user_current = req_data.user
        meberships = Membership.objects.filter(from_user = user_current)
        serializer = MemberShipSerializer(meberships,many = True)

        response.data = {
            "memberships" : serializer.data,
            "success" : True ,
            "status"  : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response