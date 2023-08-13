from django.urls import path
from . import consumers

ws_urlpatterns = [
    path('ws/sc/', consumers.MySyncConsumer_Connect.as_asgi()),
    path('ws/ac/', consumers.AsycConsumer_Connect.as_asgi()),
]
