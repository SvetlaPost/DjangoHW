from urllib import request

from django.db.models.functions.datetime import ExtractDay
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models.functions import ExtractYear

from . import models
from .models import Task, SubTask, Category
from second_app.models import Task
from .serializers import TaskSerializer, SubTaskSerializer

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from django.views.generic import TemplateView



class HomeView(TemplateView):
    template_name = 'second_app/home.html'


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


class TaskListByDayView(APIView):
    def get(self, request):
        day_of_week = request.query_params.get('day_of_week', None)

        if day_of_week:
            tasks = Task.objects.filter(day_of_week__iexact=day_of_week)
        else:
            tasks = Task.objects.all()

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubTaskListView(generics.ListAPIView):
    serializer_class = SubTaskSerializer
#    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = SubTask.objects.all().order_by('-created_at')
        main_task_name = self.request.query_params.get('main_task_name')
        status_ = self.request.query_params.get('status')

        if main_task_name:
            queryset = queryset.filter(task__title__icontains=main_task_name)

        if status_:
            queryset = queryset.filter(status=status)

        return queryset


class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        return get_object_or_404(SubTask, pk=pk)

    def get(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
