from django.urls import path, include

from chats.consumers import ChatConsumer

websocket_urlpatterns = [
    path('<uuid:group_id>/', ChatConsumer.as_asgi())

]
