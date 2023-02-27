from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.shortcuts import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import redirect_to_login
from django.views.decorators.http import require_POST
from django.views import generic
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from .models import GroupList, Invitation
from .forms import GroupListForm
from .decorators import admin_required

from chats.models import Message
from chats.models import OnlineUsers


@login_required()
def user_group_lists(request):
    groups = [*request.user.group_lists_as_admin.all(), *request.user.group_lists_as_member.all()]
    return render(request, 'group_lists/user_group_lists.html', {'groups': groups})


@login_required()
def user_group_details(request, pk):
    group = get_object_or_404(GroupList, pk=pk)
    if request.user in group.get_all_members_obj():
        previous_messages = None
        if group.enable_chat:
            previous_messages = Message.objects.filter(group=group)
        context = {'todos': group.todo.all(), 'group': group, 'group_chats': previous_messages}
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
    if request.user in group.admins.all():
        form = GroupListForm(request.user, instance=group)

        if request.method == 'POST':
            form = GroupListForm(request.user, request.POST, request.FILES, instance=group)
            if form.is_valid():
                form.save()
                messages.success(request, _("Group successfully updated"))
                return redirect('group_lists')
        return render(request, 'group_lists/group_update.html', {'form': form, 'group': group})
    raise PermissionDenied

@login_required()
@require_POST
def leave_group_view(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)

    if request.user != group.admins.first() and request.user in group.get_all_members_obj():
        if request.user in group.members.all():
            group.members.remove(request.user)
        else:
            group.admins.remove(request.user)
        messages.success(request, _('you successfully left the group'))
        return redirect('group_lists')
    raise PermissionDenied


@login_required()
@require_POST
def manage_group_users(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)

    if request.user == group.admins.first():
        user = get_object_or_404(get_user_model(), pk=list(request.POST.keys())[1])

        if user in group.members.all():
            group.members.remove(user)
            group.admins.add(user)
            messages.success(request, _('User promoted to admin'))
        elif user in group.admins.all():
            group.admins.remove(user)
            group.members.add(user)
            messages.success(request, _('User degraded to regular member'))
        else:
            messages.error(request, _('user is not a member of %s ' % group.title))
        return redirect('group_detail', group_id)
    raise PermissionDenied


@login_required()
@require_POST
@admin_required
def invite_new_members(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)
    user_ids = list(request.POST.keys())[1:]
    users = [get_object_or_404(get_user_model(), pk=pk) for pk in user_ids]
    send_group_list_invitation(request, users, group)
    messages.success(request, _("Invitations successfully sent"))
    return redirect('group_detail', group_id)


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
    return errors


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
@admin_required
def remove_user_from_list(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)
    user = get_object_or_404(get_user_model(), pk=list(request.POST.keys())[1])
    if user != group.admins.first():
        if user in group.admins.all():
            if request.user == group.admins.first():
                group.admins.remove(user)

        elif user in group.members.all():
            group.members.remove(user)

        messages.success(request, _('user successfully removed from list'))
    else:
        messages.warning(request, _('unable to remove group owner'))

    return redirect('group_detail', group.id)


def foreign_invitation_show_info(request, signed_pk):
    group = get_object_or_404(GroupList, pk=GroupList.InvLink.unsign(signed_pk))
    return render(request, 'group_lists/foreign_invite_page.html', {'group': group})


@require_POST
def accept_foreign_invite_view(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)
    if request.user.is_authenticated:

        if request.user not in group.get_all_members_obj():
            group.members.add(request.user)
            messages.success(request, _('Welcome! you are now a member of this group'))
            return redirect('group_detail', group.id)
        messages.warning(request, _('you are already in this group'))
        return redirect(group.get_invitation_link())

    return redirect_to_login(reverse('foreign_inv_show_info', args=[group.get_signed_pk()]))


@require_POST
def group_invite_user_search_view(request, group_id):
    series = str(request.POST['series'])
    group = get_object_or_404(GroupList, pk=group_id)
    users = get_user_model().objects.filter(username__icontains=series).exclude(pk__in=group.get_all_members_ids())
    if request.user in group.get_all_members_obj():
        if users and series:
            data = []
            for user in users:
                if user != request.user:
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
