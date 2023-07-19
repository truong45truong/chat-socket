from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status


# ---------------------------------------------------------------------------- #
#                           METHOD REFRESH TOKEN JWT                           #
# ---------------------------------------------------------------------------- #
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def refreshTokenJWT(request):
    response = Response()
    try:
        # ----------------------------- check information ---------------------------- #
        #decyption token jwt
        jwtToken = request.COOKIES.get('refresh_token')
        refresh_token = RefreshToken(jwtToken)
        access_token = refresh_token.access_token
        response.data = {
            'access_token' : str(access_token) , 
            'error' : { 'value' : None , 'type' : None } ,
            'status' : status.HTTP_200_OK
        }
        return response
    except:
        response.data = {
            'error' : { 'value' : "refresh token wrong" , 'type' : 'RT-0001' } ,
            'status' : status.HTTP_404_NOT_FOUND
        }
        return response
    