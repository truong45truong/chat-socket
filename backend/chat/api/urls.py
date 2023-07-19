from django.urls import path

from .views import create_conversation , get_conversation
# ---------------------------------------------------------------------------- #
#                                  METHOD URL                                  #
# ---------------------------------------------------------------------------- #

urlpatterns = [
    path('conversation/create/', create_conversation, name = "create_conversation"),
    path('conversation/', get_conversation, name = "get_conversation"),
]
