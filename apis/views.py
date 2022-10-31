from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import TodoSerializer, UserSerializer
from todo.models import Todo, Job


class Hello(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(request.POST)

        content = {'hello': 'hi'}
        return Response(content)


class TodoList(generics.ListCreateAPIView):
    serializer_class = TodoSerializer

    def get_queryset(self):
        return self.request.user.todos.all().order_by('-datetime_created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer

    def get_queryset(self):
        return self.request.user.todos.all().order_by('-datetime_created')


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
