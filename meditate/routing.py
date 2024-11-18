from django.urls import path
from . import consumerDL, consumerHRV

websocket_urlpatterns = [
    path("ws/deep_learning_analysis/", consumerDL.VideoConsumerDL.as_asgi()),  
    path("ws/heart_rate_variability/", consumerHRV.VideoConsumerHRV.as_asgi()),
]
