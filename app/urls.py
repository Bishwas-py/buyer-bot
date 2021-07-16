from django.urls import path
from.views import *

urlpatterns = [
    path("", home, name="home"),
    path("start-bot", start_bots, name="start_bot"),
]