from second_app.views import django_hello, user_hello, TaskStatsView, HomeView, TaskListCreateView, \
    TaskRetrieveUpdateDestroyView, SubtaskListCreateView, SubtaskUpdateDestroyAPIView, BulkCreateTaskView

TaskListCreateView, TaskRetrieveUpdateDestroyView
from django.urls import path

from . import views

urlpatterns = [
    path('django_hello/', django_hello, name='django_hello'),
    path('user_hello/', user_hello, name='user_hello'),

    #path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/bulk_create/', BulkCreateTaskView.as_view(), name='task-bulk-create'),

    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:id>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-list'),
    #path('tasks/by_day/', TaskListByDayView.as_view(), name='task-list-by-day'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),

    path('subtasks/', SubtaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubtaskUpdateDestroyAPIView.as_view(), name='subtask-update-delete'),

    path('', HomeView.as_view(), name='home'),

]
