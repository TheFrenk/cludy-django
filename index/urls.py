import imp
from textwrap import indent
from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('commands', commands),

]