from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.http import require_POST
from django.views import generic
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from todo.models import Todo
from pages.models import Invitation
from .models import GroupList
from .forms import GroupListForm


@login_required()
def user_group_lists(request):
    groups = [i for i in GroupList.objects.filter(users__in=[request.user]) if request.user != i.todo.user]
    return render(request, 'group_lists/user_group_lists.html', {'groups': groups})


class GroupCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = GroupList
    form_class = GroupListForm
    template_name = 'group_lists/group_create.html'
    success_url = reverse_lazy('group_lists')
    success_message = _("Group created successfully")



@login_required()
@require_POST
def leave_group_view(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)

    if request.user != group.todo.user and request.user in group.users.all():
        group.users.remove(request.user)
        messages.success(request, _('you successfully left the group'))
        return redirect('group_lists')
    raise PermissionDenied


@login_required()
@require_POST
def add_group_list_and_send_invitation(request):
    users = request.POST['users'].split(',')
    todo_id = request.POST['todo']
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.user == todo.user:
        if not todo.is_group_list():
            new_list = GroupList.objects.create(todo=todo)
            new_list.users.add(request.user)
            send_group_list_invitation(request, users, new_list)
            messages.success(request, _('group-list successfully created & invitation sent for users'))
        else:
            group_list = todo.group_todo.last()
            send_group_list_invitation(request, users, group_list)
            messages.success(request, _('invitations sent successfully'))

        return redirect('todo_settings', todo.id)

    raise PermissionDenied


def send_group_list_invitation(request, users, group_list):
    for user in users:
        try:

            user = get_object_or_404(get_user_model(), username=user)
            if not group_list.invitations.filter(user_receiver=user, user_sender=request.user).exists():

                if user not in group_list.users.all() and user != group_list.todo.user:
                    Invitation.objects.create(user_sender=request.user, user_receiver=user, group_list=group_list)
        except Exception as e:
            pass


@login_required()
@require_POST
def accept_invite(request, group_id, inv_id):
    group = get_object_or_404(GroupList, pk=group_id)
    inv = get_object_or_404(Invitation, pk=inv_id)
    if request.user == inv.user_receiver:
        group.users.add(inv.user_receiver)
        inv.delete()
        messages.success(request, _('invite accepted you are now a member of the group-list'))
        return redirect('group_lists')
    raise PermissionDenied


@login_required()
@require_POST
def remove_user_from_list(request, group_id):
    group_list = get_object_or_404(GroupList, pk=group_id)
    user = get_object_or_404(get_user_model(), pk=list(request.POST.keys())[1])
    if request.user == group_list.todo.user:
        if user in group_list.users.all() and user != group_list.todo.user:
            group_list.users.remove(user)
            messages.success(request, _('user successfully deleted from list'))
            return redirect('todo_settings', group_list.todo.id)

    raise PermissionDenied


def search_view(request):
    if request.method == 'POST':
        series = str(request.POST['series'])
        query_set = get_user_model().objects.filter(username__icontains=series)
        res = None
        if query_set and series:

            data = []

            for user in query_set:
                if user != request.user:
                    item = {
                        'pk': user.pk,
                        'username': user.username,
                    }

                    if user.profile_picture:
                        item['image'] = str(user.profile_picture.url)
                    else:
                        item['image'] = '/static/img/blank_user.png'

                    data.append(item)

            res = data
        else:
            res = 'No data'
        return JsonResponse({'data': res[:11]})
    return JsonResponse({})
