from django.urls import path

from .views import login,logout,register_user , search_user
# ---------------------------------------------------------------------------- #
#                                  METHOD URL                                  #
# ---------------------------------------------------------------------------- #

# ----------------------------------- USER ----------------------------------- #


# register_user = RegisterUserViewSet.as_view({
#     'post': 'register_user',
# })

urlpatterns = [
    path('login/', login, name = "login_user"),
    path('logout/', logout, name = "logout_user"),
    # path('user/change-password/', change_password_user, name = "change_password_user"),
    path('register-user/', register_user, name = "register_user") , 
    path('search-user/', search_user, name = "search_user") ,
]
