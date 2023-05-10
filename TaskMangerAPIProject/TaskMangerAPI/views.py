from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import UserSerializer, TaskSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, DestroyAPIView
from .models import Task
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": 'something went wrong'}, status.HTTP_403_FORBIDDEN)
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        token_obj, created = Token.objects.get_or_create(user=user)
        return Response({'result': serializer.data, 'token': str(token_obj)})


class TaskView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        data = {
            "user": user,
            "title": request.data.get("title"),
            "description": request.data.get("description"),
        }
        task = Task.objects.create(**data)
        serializer = TaskSerializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class SingleTaskView(RetrieveDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        task = Task.objects.filter(pk=kwargs.get("pk"), user=request.user)
        if not task:
            return Response({"error": "something went wrong"})
        task.delete()
        return Response({"message": "Task deleted"})

    def patch(self, request, *args, **kwargs):
        task = Task.objects.filter(pk=kwargs.get("pk"), user=request.user)
        if not task:
            return Response({"error": "something went wrong"})
        serializer = TaskSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def complete_task(request):
    tasks = Task.objects.filter(user=request.user)
    print(tasks)
    if not tasks:
        return Response({"message": "there are no task to do"})
    serialize = TaskSerializer(tasks, many=True)
    print(serialize.data)
    for task in serialize.data:
        if task["complete"]:
            return Response({"message": serialize.data})
        return Response({"message": "there are still unfinished task"})
