from django import forms
from .models import GroupList


class GroupListForm(forms.ModelForm):
    class Meta:
        model = GroupList
        fields = '__all__'
