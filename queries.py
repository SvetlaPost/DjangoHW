
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_proj.settings')
django.setup()

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from second_app.models import Task, SubTask, Category

now = timezone.now()

new_task = Task.objects.create(
    title="Prepare presentation",
    description= "Prepare materials and slides for the presentation",
    deadline = now + timedelta(days=3),

)

print(new_task.id)

subtask_1 = SubTask.objects.create(
    title="Gather information",
    description= "Find necessary information for the presentation",
    status= "new",
    deadline= now + timedelta(days=2),
    task= new_task

)

subtask_2 = SubTask.objects.create(
    title="Create slides",
    description= "Create presentation slides",
    deadline= now + timedelta(days=1),
    task= new_task
)

print("Task and SubTask created")
print(subtask_2.id)



