from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic
from django.views.decorators.http import require_POST

from chats.models import Message
from chats.models import OnlineUsers
from .decorators import admin_required
from .forms import GroupListForm
from .models import GroupList


@login_required()
def user_group_lists(request):
    groups = [*request.user.group_lists_as_admin.all(), *request.user.group_lists_as_member.all()]
    return render(request, 'group_lists/user_group_lists.html', {'groups': groups})


@login_required()
def user_group_details(request, pk):
    group = get_object_or_404(GroupList, pk=pk)
    if group.is_in_group(request.user):
        previous_messages = None
        if group.enable_chat:
            previous_messages = Message.objects.filter(group=group)
        context = {'todos': group.todos.all(), 'group': group, 'group_chats': previous_messages}
        return render(request, 'group_lists/group_detail.html', context=context)
    raise PermissionDenied


@login_required()
def create_group(request):
    form = GroupListForm(request.user)
    if request.method == 'POST':
        form = GroupListForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            form.instance.save()
            obj = form.save_todo_m2m_and_add_admin()
            if obj.enable_chat:
                OnlineUsers.objects.create(group=obj)

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
@admin_required
def group_update_view(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)
    form = GroupListForm(request.user, instance=group)
    if request.method == 'POST':

        form = GroupListForm(request.user, request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, _("Group successfully updated"))
            return redirect('group_lists')

    return render(request, 'group_lists/group_update.html', {'form': form, 'group': group})


@login_required()
@require_POST
def leave_group_view(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)
    if request.user != group.admins.first() and group.is_in_group(request.user):
        group.remove_user_from_group_by_role(request.user)
        messages.success(request, _('you successfully left the group'))
        return redirect('group_lists')
    raise PermissionDenied


@login_required()
@require_POST
def manage_group_members_grade(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)

    if group.is_owner(request.user):
        user = get_object_or_404(get_user_model(), pk=list(request.POST.keys())[1])
        if not group.is_owner(user):
            if group.is_member(user):
                group.promote_user(user)
                messages.success(request, _('User promoted to admin'))
            elif group.is_admin(user):
                group.degrade_user(user)
                messages.success(request, _('User degraded to regular member'))
            else:
                messages.error(request, _('user is not a member of %s ' % group.title))
            return redirect('group_detail', group_id)
    raise PermissionDenied


@login_required()
@require_POST
@admin_required
def remove_user_from_group(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)
    user_for_delete = get_object_or_404(get_user_model(), pk=list(request.POST.keys())[1])
    if not group.is_owner(user_for_delete):
        if group.is_admin(user_for_delete):

            if group.is_owner(request.user):
                group.admins.remove(user_for_delete)
            else:
                raise PermissionDenied

        elif group.is_member(user_for_delete):
            group.members.remove(user_for_delete)
        messages.success(request, _('user successfully removed from list'))

        return redirect('group_detail', group.id)
    raise PermissionDenied


@require_POST
def group_invite_user_search_view(request, group_id):
    series = str(request.POST['series'])
    group = get_object_or_404(GroupList, pk=group_id)
    users = get_user_model().objects.filter(username__icontains=series).exclude(pk__in=group.get_all_members_ids())

    if group.is_admin(request.user):
        if users and series:
            data = []
            for user in users:
                item = {
                    'pk': user.pk,
                    'username': user.username,
                    'image': user.get_profile_pic_or_blank()
                }
                data.append(item)

            res = data
        else:
            res = 'No data'

        return JsonResponse({'data': res})
    raise PermissionDenied
