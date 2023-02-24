from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _
from captcha.fields import ReCaptchaField


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'username']


class CustomUserChangeForm(forms.ModelForm):
    email = forms.EmailField(help_text=_('required. valid email address'),
                             widget=forms.EmailInput(attrs={'placeholder': _("Email Address")}))

    class Meta:
        model = get_user_model()
        fields = ['profile_picture', 'username', 'email']


class CustomSignupForm(forms.Form):
    captcha = ReCaptchaField()

    def signup(self, request, user):
        """ This function is required otherwise you will get an ImproperlyConfigured exception """
        pass
