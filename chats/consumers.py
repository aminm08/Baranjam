from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from channels.generic.websocket import WebsocketConsumer
from channels.consumer import AsyncConsumer
from asgiref.sync import async_to_sync
from jalali_date import date2jalali

from group_lists.models import GroupList
from .models import Message, OnlineUsers

import json


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.group = get_object_or_404(GroupList, uuid=self.scope['url_route']['kwargs']['group_id'])
        self.group_room_name = 'chat_%s' % self.group.uuid
        self.user = self.scope['user']

        self.update_online_users(self.user)

        if self.user in self.group.get_all_members_obj():
            async_to_sync(self.channel_layer.group_add)(
                self.group_room_name, self.channel_name
            )
            self.accept()

    def disconnect(self):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_room_name, self.channel_name
        )
        self.update_online_users(self.user, add=False)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        user = get_object_or_404(get_user_model(), username=text_data_json["username"])
        message_obj = self.save_message(user, text_data_json["message"], self.group)

        async_to_sync(self.channel_layer.group_send)(
            self.group_room_name,
            {'type': 'chat_message', 'message': text_data_json["message"], 'username': user.username,
             'img': user.get_profile_picture_or_blank(),
             'datetime': str(date2jalali(message_obj.datetime_created.date()))
             }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'img': event['img'],
            'datetime': event['datetime']
        }))

    def save_message(self, user, text, group):
        message = Message.objects.create(user=user, text=text, group=group)
        return message

    def update_online_users(self, user, add=True):
        online_user_obj = OnlineUsers.objects.get(group=self.group)

        if add:
            online_user_obj.online_users.add(user)
        else:
            online_user_obj.online_users.remove(user)
