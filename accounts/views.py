from django.shortcuts import render
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserChangeForm


class DashBoard(generic.TemplateView):
    template_name = ''


def user_profile(request):
    form = CustomUserChangeForm(instance=request.user)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('your profile updated successfully'))
    return render(request, 'account/profile.html', {'form': form})
