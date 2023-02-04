import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from chats import routing

application = ProtocolTypeRouter(
    {
        "http": asgi_app,
        "websocket": AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))

    }
)
