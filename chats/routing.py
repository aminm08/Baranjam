from django.urls import path, include

from chats.consumers import ChatConsumer

websocket_urlpatterns = [
    path('<slug:room_slug>/', ChatConsumer.as_asgi())

]
