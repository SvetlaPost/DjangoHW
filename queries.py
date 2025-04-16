
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
#
##print(new_task.id)
#
#subtask_1 = SubTask.objects.create(
#    title="Gather information",
#    description= "Find necessary information for the presentation",
#    status= "new",
#    deadline= now + timedelta(days=2),
#    task= new_task)

subtask_2 = SubTask.objects.create(
    title="Create slides",
    description= "Create presentation slides",
    deadline= now + timedelta(days=1),
    task= new_task
)
print("Task and SubTask created")
print(subtask_2.id)

#Чтение записей:

#new_task = Task.objects.filter(status='new')
#for t in new_task:
#    print(f"{t.id}: {t.title}")

from django.http import HttpResponse, HttpRequest
from django.utils import timezone
from second_app.models import SubTask

#def overdue_done_subtasks(request):
#    now = timezone.now()
#    overdue_done = SubTask.objects.filter(status="done", deadline__lt=now)
#
#    if not overdue_done:
#        return HttpResponse("<h1>Нет просроченных выполненных подзадач</h1>")
#
#    response = "<h1>Overdue Done Subtasks</h1>"
#    for subtask in overdue_done:
#        response += f"<p>{subtask.title} — Deadline: {subtask.deadline}</p>"
#
#    return HttpResponse(response)
#
#if __name__ == "__main__":
#    fake_request = HttpRequest()
#    result = overdue_done_subtasks(fake_request)
#    print(result.content.decode())
#

#Изменение записей:

#prepare_presentation = Task.objects.get(id__in="1")
#prepare_presentation.status = "In progress"
#prepare_presentation.save()

#subtask = SubTask.objects.get(id=1)
#
#new_deadline = subtask.deadline - timedelta(days=2)
#
#subtask.deadline = new_deadline
#subtask.save()

#print(f"Новый дедлайн для подзадачи '{subtask.title}': {subtask.deadline}")

#subtask = SubTask.objects.get(id=2)
#subtask.description = "Create and format presentation slides"
#subtask.save()

#Удаление записей:

#deleted_task = Task.objects.get(id=1)
#deleted_task.delete()

try:
    deleted_task = Task.objects.get(id=1)
    deleted_task.delete()
    print("Задача успешно удалена.")
except Task.DoesNotExist:
    print("Задача с таким ID не найдена.")





