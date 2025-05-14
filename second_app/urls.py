from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    CategoryViewSet,
    TaskListCreateView,
    TaskRetrieveUpdateDestroyView,
    BulkCreateTaskView,
    TaskStatsView,
    SubtaskListCreateView,
    SubtaskUpdateDestroyAPIView,
    HomeView,
    django_hello,
    user_hello,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('django_hello/', django_hello, name='django_hello'),
    path('user_hello/', user_hello, name='user_hello'),
    path('tasks/bulk_create/', BulkCreateTaskView.as_view(), name='task-bulk-create'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:id>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-list'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('subtasks/', SubtaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubtaskUpdateDestroyAPIView.as_view(), name='subtask-update-delete'),
    path('', HomeView.as_view(), name='home'),
    path('auth-login/', obtain_auth_token),
    path('auth-login-jwt/', TokenObtainPairView.as_view()),
    path('token-refresh/', TokenRefreshView.as_view()),
] + router.urls



