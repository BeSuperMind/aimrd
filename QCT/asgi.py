import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from meditate.consumerDL import VideoConsumerDL  
from meditate.consumerHRV import VideoConsumerHRV
from django.urls import path


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QCT.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # Define your WebSocket URL routing here
            path('ws/deep_learning_analysis/', VideoConsumerDL.as_asgi()), 
            path('ws/heart_rate_variability/', VideoConsumerHRV.as_asgi()), 
        ])
    ),
})
