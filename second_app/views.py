from urllib import request
from django.http import HttpResponse

from . import models
from .models import Task, SubTask, Category

from rest_framework import generics
from second_app.models import Task
from .serializers import TaskSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone


def django_hello(request) -> HttpResponse:
    return HttpResponse(
        "<h1>Greetings from the Django APP!!! :)</h1>"
    )

def user_hello(request):
    name = "Svetlana"
    return HttpResponse(
        f"<h2>Greetings {name}!!! :)</h2>"
    )

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'

class TaskStatsView(APIView):
    def get(self, request):
        total_tasks = Task.objects.count()
        by_status = Task.objects.values('status').annotate(count=models.Count('id'))
        overdue = Task.objects.filter(deadline__lt=timezone.now()).count()

        return Response({
            'total_tasks': total_tasks,
            'tasks_by_status': by_status,
            'overdue_tasks': overdue,
        })
