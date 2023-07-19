from django.urls import path

from .views import refreshTokenJWT


urlpatterns = [
    path('token/refresh/', refreshTokenJWT, name = "refresh_token_jwt") # api refresh token access
]
