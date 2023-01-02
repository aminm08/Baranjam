from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from .utils import *

from .forms import ContactForm
from .models import Contact


def homepage(request):
    return render(request, 'homepage.html')


def about_us(request):
    return render(request, 'about_us.html')


class ContactUs(SuccessMessageMixin, generic.CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact_us.html'
    success_url = reverse_lazy('contact_us')
    success_message = _('successfully sent')

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        obj_form = form.save(commit=False)
        if self.request.user.is_authenticated:
            obj_form.user = self.request.user
        obj_form.ip_addr = get_client_ip_address(self.request)
        obj_form.save()
        return super().form_valid(form)
