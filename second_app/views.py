from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics, status, filters, viewsets
from rest_framework.response import Response
from rest_framework.request import  Request
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import (LimitOffsetPagination,
                                       CursorPagination,
                                       )
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from second_app import models
from second_app.models import Task, SubTask, Category
from second_app.serializers import (TaskSerializer,
                          SubTaskSerializer,
                          TaskCreateSerializer,
                          Category)




from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     ListAPIView)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from.permissions import (
    IsAdminOrReadOnly,
    IsOwnerOrReadOnly,
    IsAdminWithMessage,
    IsOwner,
)
from rest_framework.permissions import AllowAny
from .serializers import CategorySerializer, RegisterSerializer



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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

#CATEGORIES

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        count = category.tasks.count()
        return Response({'task_count': count})


#TASKS

class UserTaskListView(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):

        return Task.objects.filter(owner=self.request.user)


class BulkCreateTaskView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CursorPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        day_of_week = self.request.query_params.get('day_of_week')

        if day_of_week:
            queryset = queryset.filter(day_of_week__iexact=day_of_week)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'id'


#class TaskListView(generics.ListAPIView):
#    queryset = Task.objects.all()
#    serializer_class = TaskSerializer

#class TaskDetailView(generics.RetrieveAPIView):
#    queryset = Task.objects.all()
#    serializer_class = TaskSerializer
#    lookup_field = 'id'

class TaskStatsView(APIView):
    permission_classes = [IsAdminWithMessage]

    def get(self, request):
        total_tasks = Task.objects.count()
        by_status = Task.objects.values('status').annotate(count=models.Count('id'))
        overdue = Task.objects.filter(deadline__lt=timezone.now()).count()

        return Response({
            'total_tasks': total_tasks,
            'tasks_by_status': by_status,
            'overdue_tasks': overdue,
        })

#class TaskListByDayView(APIView):
#    def get(self, request):
#        day_of_week = request.query_params.get('day_of_week', None)
#
#        if day_of_week:
#            tasks = Task.objects.filter(day_of_week__iexact=day_of_week)
#        else:
#            tasks = Task.objects.all()
#
#        serializer = TaskSerializer(tasks, many=True)
#        return Response(serializer.data, status=status.HTTP_200_OK)

#SUBTASKS

class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user)


class SubtaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubtaskUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'pk'



#class SubTaskListView(generics.ListAPIView):
#    serializer_class = SubTaskSerializer
##    pagination_class = LimitOffsetPagination
#
#    def get_queryset(self):
#        queryset = SubTask.objects.all().order_by('-created_at')
#        main_task_name = self.request.query_params.get('main_task_name')
#        status_ = self.request.query_params.get('status')
#
#        if main_task_name:
#            queryset = queryset.filter(task__title__icontains=main_task_name)
#
#        if status_:
#            queryset = queryset.filter(status=status)
#
#        return queryset
#
#
#class SubTaskListCreateView(APIView):
#    def get(self, request):
#        subtasks = SubTask.objects.all()
#        serializer = SubTaskSerializer(subtasks, many=True)
#        return Response(serializer.data)
#
#    def post(self, request):
#        serializer = SubTaskSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

#class SubTaskDetailUpdateDeleteView(APIView):
#    def get_object(self, pk):
#        return get_object_or_404(SubTask, pk=pk)

#    def get(self, request, pk):
#        subtask = self.get_object(pk)
#        serializer = SubTaskSerializer(subtask)
#        return Response(serializer.data)

#    def put(self, request, pk):
#        subtask = self.get_object(pk)
#        serializer = SubTaskSerializer(subtask, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    def delete(self, request, pk):
#        subtask = self.get_object(pk)
#        subtask.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
