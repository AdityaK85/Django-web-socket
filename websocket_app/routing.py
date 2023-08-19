from django.urls import path
from . import consumers

ws_urlpatterns = [
    path('ws/sc/<str:group_name>/', consumers.MySyncConsumer_Connect.as_asgi()),
    path('ws/ac/<str:group_name>/', consumers.AsycConsumer_Connect.as_asgi()),

    # Generic consumer
    path('ws/gsc/<str:group_name>/', consumers.New_WebSocket_Consumer.as_asgi()),
    path('ws/gac/<str:group_name>/', consumers.New_Async_WebSocket_Consumer.as_asgi()),

    # Generic Json Websocket consumer
    path('ws/gjsc/<str:group_name>/', consumers.my_Json_Websockete_Consumer.as_asgi()),
    path('ws/gjac/<str:group_name>/', consumers.my_Async_Json_Websockete_Consumer.as_asgi()),
    
]
