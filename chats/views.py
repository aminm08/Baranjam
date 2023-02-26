from django.shortcuts import render, get_object_or_404
from group_lists.models import GroupList
from .models import OnlineUsers
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

@login_required()
def get_group_online_users(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)
    if request.user in group.get_all_members_obj() and group.enable_chat:

        data = []
        online_group_obj = get_object_or_404(OnlineUsers, group=group)
        for user in online_group_obj.online_users.all():
            data.append([user.username, user.get_profile_pic_or_blank()])

        return JsonResponse(data, safe=False)
    raise PermissionDenied
