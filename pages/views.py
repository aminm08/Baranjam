from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from todo.models import Todo


def homepage(request):
    return render(request, 'homepage.html')


def about_us(request):
    return render(request, 'about_us.html')


def contact_us(request):
    return render(request, 'contact_us.html')


@login_required
def dashboard_view(request):
    user_todos = Todo.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'todos': user_todos})
