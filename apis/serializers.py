from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from todo.models import Todo, Job


class TodoSerializer(ModelSerializer):
    class Meta:
        model = Todo
        fields = ['name']


class JobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = ['text', 'todo', 'user', 'is_done', 'user_datetime']


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'birth_date', 'profile_picture', 'first_name', 'last_name']
