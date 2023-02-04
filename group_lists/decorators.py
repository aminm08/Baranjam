from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import GroupList


def admin_required(view):
    def _view(request, *args, **kwargs):
        group = get_object_or_404(GroupList, pk=int(kwargs['group_id']))
        if request.user not in group.admins.all():
            raise PermissionDenied
        return view(request, *args, **kwargs)

    return _view
