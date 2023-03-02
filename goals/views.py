from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from .forms import GoalForm
from .models import Goal
from django.utils.translation import gettext as _
from django.contrib import messages


class GoalCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    form_class = GoalForm
    model = Goal
    http_method_names = ['post']
    success_url = reverse_lazy('dashboard')
    success_message = _("Goal successfully added")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, str(form.errors))
        return redirect('dashboard')


class GoalDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    model = Goal
    http_method_names = ['post']
    success_url = reverse_lazy('dashboard')
    success_message = _('goal successfully deleted')

    def test_func(self):
        return self.request.user == self.get_object().user
