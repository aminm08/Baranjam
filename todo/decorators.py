from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Todo


def list_owner_only(view):
    def _view(request, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=int(kwargs['todo_id']))
        if todo.is_owner(request.user):
            return view(request, *args, **kwargs)
        raise PermissionDenied

    return _view
