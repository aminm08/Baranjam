import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from .models import Message
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from group_lists.models import GroupList


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room = get_object_or_404(GroupList, slug=self.scope['url_route']['kwargs']['room_slug'])
        self.room_name = self.room.slug
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        user = get_object_or_404(get_user_model(), username=username)
        img = user.profile_picture.url if user.profile_picture else '/static/img/blank_user.png'
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {'type': 'chat_message', 'message': message, 'username': username, 'img': img}
        )
        self.save_message(user, message, self.room)

    def chat_message(self, event):
        message = event['message']
        username = event['username']
        img = event['img']

        self.send(text_data=json.dumps({'message': message, 'username': username, 'img': img}))

    def save_message(self, user, text, group):
        Message.objects.create(user=user, text=text, group=group)
