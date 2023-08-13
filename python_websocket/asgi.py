import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import websocket_app.routing
import websocket_app.urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_websocket.settings')
print("server is running on asgi")
application = ProtocolTypeRouter({

    'http':get_asgi_application(),
    'websocket': URLRouter(
        websocket_app.routing.ws_urlpatterns
    )
})
