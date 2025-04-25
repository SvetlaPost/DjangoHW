from second_app.views import django_hello, user_hello, TaskListView, TaskDetailView, TaskStatsView
from django.urls import path
from .views import TaskCreateView
from . import views

urlpatterns = [
    path('django_hello/', django_hello, name='django_hello'),
    path('user_hello/', user_hello, name='user_hello'),

    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:id>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
]


