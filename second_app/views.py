from urllib import request
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, SubTask, Category
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

from .models import Task, SubTask


def django_hello(request) -> HttpResponse:
    return HttpResponse(
        "<h1>Greetings from the Django APP!!! :)</h1>"
    )

def user_hello(request):
    name = "Svetlana"
    return HttpResponse(
        f"<h2>Greetings {name}!!! :)</h2>"
    )

