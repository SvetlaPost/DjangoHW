from django.urls import path
from django.urls.conf import include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

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
    user_hello, UserTaskListView,
    RegisterView, LogoutView,
)

schema_view = get_schema_view(
    openapi.Info(
        title='Tasks_API',
        default_version='v1',
        description='Документация к вашему API',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='test.email@gmail.com'),
        license=openapi.License(name='OUR LICENSE', url='example.com',),
    ),
        public=True,
        permission_classes=[permissions.AllowAny,],
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
    #path('user-tasks/', UserTaskListView.as_view()),
    path("register/", RegisterView.as_view(), name="register"),
    path('auth-login/', obtain_auth_token),
    path('access-login-jwt/', TokenObtainPairView.as_view()),
    path('token-refresh/', TokenRefreshView.as_view()),
    path("logout/", LogoutView.as_view(), name="logout"),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    #path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + router.urls



