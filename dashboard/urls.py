from textwrap import indent
from django.urls import path

from .views import *

urlpatterns = [
    path('dashboard', get_authenticated_user, name='get_authenticated_user'),
    path('oauth2/', home, name="oauth2"),
    path('oauth2/login', discord_login, name="ouath_login"),
    path('oauth2/logout', discord_logout, name="ouath_logout"),
    path('oauth2/login/redirect', discord_login_redirect, name="discord_login_redirect")
]