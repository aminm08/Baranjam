from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from group_lists.decorators import admin_required
from group_lists.models import GroupList
from .models import Invitation


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


@login_required()
def delete_invitation_view(request, inv_id):
    invitation = get_object_or_404(Invitation, pk=inv_id)
    if invitation.user_receiver == request.user:
        invitation.delete()
        return redirect('homepage')
    raise PermissionDenied


@require_POST
def accept_foreign_invite_view(request, group_id):
    group = get_object_or_404(GroupList, pk=group_id)
    if request.user.is_authenticated:
        if not group.is_in_group(request.user):
            group.members.add(request.user)
            messages.success(request, _('Welcome! you are now a member of this group'))
            return redirect('group_detail', group.id)
        messages.warning(request, _('you are already in this group'))
        return redirect(group.get_invitation_link())

    return redirect_to_login(reverse('foreign_inv_show_info', args=[group.get_signed_pk()]))


def foreign_invitation_show_info(request, signed_pk):
    group = get_object_or_404(GroupList, pk=GroupList.InvLink.unsign(signed_pk))
    return render(request, 'invitations/foreign_invite_page.html', {'group': group})


@login_required()
@require_POST
def accept_invite(request, group_id, inv_id):
    group = get_object_or_404(GroupList, pk=group_id)
    inv = get_object_or_404(Invitation, pk=inv_id)
    if inv.is_user_valid_for_accept(request.user):
        if not group.is_in_group(request.user):
            group.members.add(inv.user_receiver)
            inv.delete()
            messages.success(request, _('invite accepted you are now a member of the group-list'))
        else:
            messages.error(request, _('you are already in this group'))
        return redirect('group_lists')
    raise PermissionDenied


def send_group_list_invitation(request, users, group_list):
    errors = {}
    for user in users:
        if not group_list.is_in_group(user):
            if not group_list.user_has_invitation(sender=request.user, receiver=user):
                Invitation.objects.create(user_sender=request.user, user_receiver=user, group_list=group_list)
            else:
                errors[user] = 'is already invited'
        else:
            errors[user] = 'is already in the group'
    return errors
