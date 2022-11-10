from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q
from .models import GroupList
from todo.models import Todo
from .forms import GroupListForm
from pages.models import Invitation


def add_user_with_invite_to_group_list_view(request):
    form = GroupListForm()
    user_groups = GroupList.objects.filter(Q(todo__in=request.user.todos.all())| Q())
    if request.method == 'POST':
        users = request.POST['users']
        todo_id = int(request.POST['todo'])
        users = get_object_or_404(get_user_model(), username=users)
        todo = get_object_or_404(Todo, pk=todo_id)
        list = GroupList.objects.create(todo=todo)

        inv = Invitation.objects.create(user_sender=request.user, user_receiver=users, group_list=list)

    return render(request, 'group_lists/add_group_list.html', {'form': form, 'user_groups':user_groups})



def search_view(request):
    if request.method == 'POST':
        series = str(request.POST['series'])
        query_set = get_user_model().objects.filter(username__icontains=series)
        res = None
        if query_set and series:

            data = []

            for user in query_set:
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


def accept_invite(request, group_id):
    if request.method == 'POST':
        group = get_object_or_404(GroupList, pk=group_id)
        group.users.add(request.user)
        return redirect('homepage')
