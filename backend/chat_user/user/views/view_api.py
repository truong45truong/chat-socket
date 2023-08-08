from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework import status
from rest_framework.response import Response
from chat_base.core.middlewares.authenticate import CustomAuthentication
from chat_user.user.services.services_user import UserService

#LOGIN
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def login(request):
    userSerice =  UserService()
    return userSerice.login(request)
    
#LOGOUT
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
    userSerice =  UserService()
    return userSerice.register(request)

#SEARCH USER
@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def search_user(request):
    userSerice =  UserService()
    return userSerice.search_user(request)

#ADD MEMBER SHIP
@api_view(['POST'])
@authentication_classes([CustomAuthentication])
def add_friend(request):
    userSerice =  UserService()
    return userSerice.add_member_ship(request)

#GET ALL MEMBER SHIP
@api_view(['GET'])
@authentication_classes([CustomAuthentication])
def get_all_membership(request):
    userSerice =  UserService()
    return userSerice.get_all_member_ship(request)