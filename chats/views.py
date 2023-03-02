from django.shortcuts import redirect, get_object_or_404
from group_lists.models import GroupList
from .models import OnlineUsers
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST


@login_required()
def get_group_online_users(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)
    if group.is_in_group(request.user) and group.enable_chat:
        data = []
        online_users_obj = get_object_or_404(OnlineUsers, group=group)
        for user in online_users_obj.online_users.all():
            data.append([user.username, user.get_profile_pic_or_blank()])

        return JsonResponse(data, safe=False)
    raise PermissionDenied


@login_required()
@require_POST
def delete_group_chat_history(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)
    if request.user in group.admins.all():
        group.messages.all().delete()
        messages.success(request, _("Group chat successfully cleared"))
        return redirect(group.get_absolute_url())
    raise PermissionDenied
