from django.shortcuts import render, get_object_or_404
from group_lists.models import GroupList
from .models import OnlineUsers
from django.http import JsonResponse
import json


def get_group_online_users(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)
    if request.user in group.get_all_members_obj():
        if group.enable_chat:
            online_group_obj = get_object_or_404(OnlineUsers, group=group)
            data = []
            for user in online_group_obj.online_users.all():
                data.append([user.username, user.get_profile_pic_or_blank()])
            print(data)
            return JsonResponse(data, safe=False)



