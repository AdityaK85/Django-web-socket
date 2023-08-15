from django.urls import path
from . import consumers

ws_urlpatterns = [
    path('ws/sc/<str:group_name>/', consumers.MySyncConsumer_Connect.as_asgi()),
    path('ws/ac/<str:group_name>/', consumers.AsycConsumer_Connect.as_asgi()),
]
