from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from feeds.consumers import FeedConsumer
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # Include WebSocket routing for your consumers here
            path("ws/feeds/", FeedConsumer.as_asgi()),
        ])
    ),
})
