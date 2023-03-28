from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from .forms import HabitForm
from .models import Habit


class HabitListView(LoginRequiredMixin, generic.ListView):
    model = Habit
    template_name = "habits/habit_list.html"
    context_object_name = 'habits'

    def get_queryset(self):
        return self.request.user.habits.all().order_by('-datetime_created')


@login_required()
def habit_create_view(request):
    form = HabitForm(request.user)
    if request.method == 'POST':
        form = HabitForm(request.user, request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, _('Habit successfully created'))
            return redirect('user_todos')
    return render(request, "habits/habit_create.html", {'form': form})


class HabitDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    model = Habit
    template_name = "habits/habit_delete.html"
    context_object_name = 'habit'
    success_url = reverse_lazy('user_todos')
    success_message = _("Habit successfully deleted")

    def test_func(self):
        return self.get_object().user == self.request.user


@login_required()
def habit_update_view(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    if habit.user == request.user:
        form = HabitForm(request.user, instance=habit)
        if request.method == 'POST':
            form = HabitForm(request.user, request.POST, instance=habit)
            if form.is_valid():
                form.save()
                messages.success(request, _('Habit successfully updated'))
                return redirect('user_todos')
        return render(request, "habits/habit_update.html", {'form': form, 'habit': habit})
    raise PermissionDenied
