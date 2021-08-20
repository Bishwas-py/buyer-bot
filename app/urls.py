from django.urls import path
from.views import *

urlpatterns = [
    path("", home, name="dashboard"),
    path("clear-bots/", clear_bots, name="clear_bots"),
    path("stop-all/", stop_all_bots, name="stop_all_bots"),
    path("start-bots/", start_bots, name="start_bot"),
    path("stop-bot/<int:id>/", stop_bots, name="stop"),
    path("start-bot/<int:id>/", start_iso_bot, name="start"),
]