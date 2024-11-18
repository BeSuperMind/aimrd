from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from meditate.routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handle HTTP connections as usual
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Route WebSocket connections to `meditate` app
        )
    ),
})
