from second_app.views import django_hello, user_hello
from django.urls import path
from . import views

urlpatterns = [
    path('django_hello/', django_hello, name='django_hello'),
    path('user_hello/', user_hello, name='user_hello'),
]
