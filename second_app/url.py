from second_app.views import django_hello, user_hello, TaskListView, TaskDetailView, TaskStatsView, HomeView
from django.urls import path
from .views import TaskCreateView, SubTaskListCreateView, SubTaskDetailUpdateDeleteView, TaskListByDayView
from . import views

urlpatterns = [
    path('django_hello/', django_hello, name='django_hello'),
    path('user_hello/', user_hello, name='user_hello'),

    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:id>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),

    path('', HomeView.as_view(), name='home'),

    path('tasks/by_day/', TaskListByDayView.as_view(), name='task-list-by-day'),

]
