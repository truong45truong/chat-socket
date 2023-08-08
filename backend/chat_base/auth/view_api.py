from rest_framework.decorators import api_view,permission_classes,authentication_classes
from .services import AuthService


# ---------------------------------------------------------------------------- #
#                           METHOD REFRESH TOKEN JWT                           #
# ---------------------------------------------------------------------------- #
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def refreshTokenJWT(request):
    authService = AuthService()
    return authService.refresh_token(request)
    