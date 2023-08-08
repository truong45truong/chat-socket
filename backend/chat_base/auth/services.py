from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status


class AuthService:
    def __init__(self):
        super(AuthService,self).__init__()
          
    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    def refresh_token(self,req_data):
        response = Response()
        jwtToken = req_data.COOKIES.get('refresh_token')
        refresh_token = RefreshToken(jwtToken)
        access_token = refresh_token.access_token
        response.data = {
            'access_token' : str(access_token) , 
            'error' : { 'value' : None , 'type' : None } ,
            'status' : status.HTTP_200_OK
        }
        return response
    