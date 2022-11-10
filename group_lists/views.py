from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
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


@login_required()
def user_group_lists(request):
    groups = GroupList.objects.filter(users__in=[request.user])
    return render(request, 'group_lists/add_group_list.html', {'groups': groups})


@login_required()
@require_POST
def add_group_list_and_send_invitation(request):
    user, todo_id = request.POST['users'], request.POST['todo']
    todo = get_object_or_404(Todo, pk=todo_id)
    user = get_object_or_404(get_user_model(), username=user)

    if not GroupList.objects.filter(todo=todo).exists() and user != request.user:
        new_list = GroupList.objects.create(todo=todo)
        new_list.users.add(request.user)
        Invitation.objects.create(user_sender=request.user, user_receiver=user, group_list=new_list)
        messages.success(request, _('group-list successfully created & invitation sent for users'))
    else:
        messages.error(request, _('this list is already in a group'))

    return redirect('group_lists')


class DeleteGroupList(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    model = GroupList
    http_method_names = ['post']
    success_url = reverse_lazy('group_lists')
    success_message = _('Group list successfully deleted')

    def test_func(self):
        return self.request.user == self.get_object().todo.user


@login_required()
@require_POST
def accept_invite(request, group_id, inv_id):
    group = get_object_or_404(GroupList, pk=group_id)
    inv = get_object_or_404(Invitation, pk=inv_id)
    group.users.add(inv.user_receiver)
    inv.delete()
    messages.success(request, _('invite accepted you are now a member of the group-list'))
    return redirect('group_lists')


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
        return JsonResponse({'data': res})
    return JsonResponse({})
