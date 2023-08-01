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
from user.models import User , Membership
from .serializers import UserSerializer , MemberShipSerializer
import uuid
import json
import base64
import uuid 
import os

# ---------------------------------------------------------------------------- #
#                                  LOGIN USER                                  #
# ---------------------------------------------------------------------------- #
@api_view(['POST'])
def login(request):
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
    }
    
    data_request= json.loads(request.body.decode('utf-8'))
    print(data_request)
    response = Response()
    username = data_request['username']
    password = data_request['password']
    

    user = authenticate(username=username, password=password)
    #check username
    if user is not None:
        if user.is_active:
            queryset = User.objects.get(username = username)
            tokens = get_tokens_for_user(user)
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=tokens["refresh"],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            csrf.get_token(request)
            serializer = UserSerializer(queryset,many = False)
            response.data = {
                "success" : "login success" , "access_token" : tokens["access"] ,
                "user" : serializer.data ,'status' : status.HTTP_200_OK
            }
            response.status_code = status.HTTP_200_OK
            return response
        else:
            return Response({"No active" : "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"Invalid" : "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)
    
# ---------------------------------------------------------------------------- #
#                                  LOGOUT USER                                 #
# ---------------------------------------------------------------------------- #
@api_view(['POST'])
def logout(request):
    try:
        response = Response()
        response.delete_cookie('refresh_token')
        response.delete_cookie('csrftoken')
        response.data = {
            "success" : "Logout success" , "status" : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
    except Exception as e :
        print(e)
        response.data = {
            "success" : "Logout failure" , "status" : status.HTTP_404_NOT_FOUND
        }
        response.status_code = status.HTTP_404_NOT_FOUND
    return response


# REGISTER USER

@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def register_user(request):
    response = Response()
    list_name_file_blog = []
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
    }
    # ---------------------------- check params input ---------------------------- #
    try:
        data_request= json.loads(request.body.decode('utf-8'))
        username = data_request['username']
        name = data_request['name']
        email    = data_request['email']
        password = data_request['password']

        if (
            username == '' 
            or name == ''
            or email == ''
            or password == ''
        ):  
            print(data_request)
            return Response({ 
                'user' : False , 'status' : status.HTTP_404_NOT_FOUND ,
                'error' : { 'value' : 'Params input wrong' , 'type' : 'RU-0000' }
            })
    except Exception as e:
        print(e)
        return Response({ 
            'user' : False , 'status' : status.HTTP_404_NOT_FOUND ,
            'error' : { 'value' : 'Params input wrong' , 'type' : 'RU-0000' }
        })
    # -------------------------------- create user ------------------------------- #
    # check username
    try:
        user = User.objects.create(
            username=username,photo = None ,
            name = name
        )
        user.password  = make_password(password)
        user.save()  
    except Exception as e:
        print(e)
        return Response({ 
            'user' : False , 'status' : status.HTTP_404_NOT_FOUND ,
            'error' : { 'value' : 'Username available' , 'type' : 'RU-0001' }
        })
    # check email
    try:
        user.email = email
        user.save()
    except:
        user.delete()
        return Response({ 
            'user' : False , 'status' : status.HTTP_404_NOT_FOUND ,
            'error' : { 'value' : 'Email available' , 'type' : 'RU-0002' }
        })

    # ------------------------------ end create user ----------------------------- #
    try:
        tokens = get_tokens_for_user(user)
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=tokens["refresh"],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        csrf.get_token(request)
        serializer = UserSerializer(user,many = False)
        response.data = {
            "success" : "register success" , "access_token" : tokens["access"] ,
            "user" : serializer.data ,'status' : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    except:
        return Response({ 
            'user' : False , 'status' : status.HTTP_404_NOT_FOUND ,
            'error' : { 'value' : 'Information Wrong' , 'type' : 'RU-0004' }
        })

#SEARCH USER

@api_view(['GET'])
def search_user(request):
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
    def getUsers(key_search):
        userSearches = User.objects.filter(email__icontains=key_search)[:5]
        serializer = UserSerializer(userSearches,many = True)

        response.data = {
            "users" : serializer.data,
            "success" : True ,
            "status"  : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    try:
        key_search = request.GET.get('key_search')

        return getUsers(key_search)
    except Exception as e :
        return notFound()
    
@api_view(['POST'])
def add_friend(request):
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
    def AddMemberShip(user_added , userCurrent):
        userAdded = User.objects.get(email=user_added)
        checkMember = Membership.objects.filter(from_user = userCurrent , to_user = userAdded)
        if len(checkMember) > 0:
            checkMember[0].delete()
        else:
            memberShip = Membership.objects.create(
                from_user = userCurrent , 
                to_user = userAdded,
            )

        response.data = {
            "success" : True ,
            "status"  : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    try:
        data_request= json.loads(request.body.decode('utf-8'))
        user_added = data_request['user_to']
        jwtToken = request.COOKIES.get('refresh_token')
        refresh_token = RefreshToken(jwtToken)
        decoded_token = refresh_token.payload
        userCurrent = User.objects.get(id = decoded_token['user_id'])
        return AddMemberShip(user_added , userCurrent)
    except Exception as e :
        return notFound()

@api_view(['GET'])
@permission_classes([])
@authentication_classes([JWTAuthentication])
def get_all_membership(request):
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
    def getMemberShip(userCurrent):
        meberships = Membership.objects.filter(from_user = userCurrent)
        serializer = MemberShipSerializer(meberships,many = True)

        response.data = {
            "memberships" : serializer.data,
            "success" : True ,
            "status"  : status.HTTP_200_OK
        }
        response.status_code = status.HTTP_200_OK
        return response
    try:
        jwtToken = request.COOKIES.get('refresh_token')
        refresh_token = RefreshToken(jwtToken)
        decoded_token = refresh_token.payload
        userCurrent = User.objects.get(id = decoded_token['user_id'])
        return getMemberShip(userCurrent)
    except Exception as e :
        print(e)
        return notFound()