from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
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
    groups = [*request.user.as_member.all(), *request.user.as_admin.all()]
    return render(request, 'group_lists/user_group_lists.html', {'groups': groups})


@login_required()
def user_group_details(request, pk):
    group = get_object_or_404(GroupList, pk=pk)
    print(group.get_all_members_obj())
    return render(request, 'group_lists/group_detail.html',
                  {'todos': group.todo.all(), 'group': group,
                   'all_users': [user for user in get_user_model().objects.all() if
                                 user not in group.get_all_members_obj()]})


@login_required()
def create_group(request):
    form = GroupListForm(request.user)
    if request.method == 'POST':
        form = GroupListForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            data = form.cleaned_data

            send_group_list_invitation(request, data['members'], form.instance)
            messages.success(request, _("Group created successfully and invitations are sent"))
            return redirect('group_lists')
    return render(request, 'group_lists/group_create.html', {'form': form})


class GroupDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    model = GroupList
    template_name = 'group_lists/group_delete.html'
    context_object_name = 'group'
    success_url = reverse_lazy('group_lists')
    success_message = _('group successfully removed')

    def test_func(self):
        return self.request.user == self.get_object().admins.first()


@login_required()
def group_update_view(request, pk):
    group = get_object_or_404(GroupList, pk=pk)

    if request.user in group.admins.all():
        form = GroupListForm(request.user, instance=group, exclude_members=True)

        if request.method == 'POST':
            form = GroupListForm(request.user, request.POST, instance=group, exclude_members=True)

            if form.is_valid():
                form.save(create=False)

                messages.success(request, _("Group successfully updated"))
                return redirect('group_lists')
        return render(request, 'group_lists/group_update.html', {'form': form, 'group': group})
    raise PermissionDenied


# member 2 admin
# invite new users
# invite link


@login_required()
@require_POST
def leave_group_view(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)

    if request.user != group.todo.user and request.user in group.users.all():
        group.members.remove(request.user)
        messages.success(request, _('you successfully left the group'))
        return redirect('group_lists')
    raise PermissionDenied


@login_required()
@require_POST
def add_admin(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)

    if request.user in group.admins.all():
        user_ids = list(request.POST.keys())[1:]

        for id in user_ids:
            user = get_object_or_404(get_user_model(), pk=id)
            if user not in group.members.all():
                continue

            if user not in group.admins.all():
                group.members.remove(user)
                group.admins.add(user)
        return redirect('group_detail', group_id)
    raise PermissionDenied


@login_required()
@require_POST
def invite_new_members(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)

    if request.user in group.admins.all():
        user_ids = list(request.POST.keys())[1:]
        users = [get_object_or_404(get_user_model(), pk=pk) for pk in user_ids]
        send_group_list_invitation(request, users, group)
        return redirect('group_detail', group_id)
    raise PermissionDenied


def send_group_list_invitation(request, users, group_list):
    errors = {}
    for user in users:

        if user not in group_list.members.all():
            if not group_list.invitations.filter(user_receiver=user, user_sender=request.user).exists():
                Invitation.objects.create(user_sender=request.user, user_receiver=user, group_list=group_list)
            else:
                errors[user] = 'is already invited'
        else:
            errors[user] = 'is already in the group'
    print(errors)


@login_required()
@require_POST
def accept_invite(request, group_id, inv_id):
    group = get_object_or_404(GroupList, pk=group_id)
    inv = get_object_or_404(Invitation, pk=inv_id)
    if request.user == inv.user_receiver:
        group.members.add(inv.user_receiver)
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
