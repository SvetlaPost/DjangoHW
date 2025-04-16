from django.contrib.auth.models import User
from django.db import models

#user = User(
#    username="NEWUniqueUser",
#    email="newunique.email@gmail.com",
#    first_name="Unique2",
#    last_name="User2",
#)
#user.set_password("as-0dG<y0S8^d7fgtS<78")
#
#user.save()

class Category(models.Model):
    STATUS_CHOICES = [
        ('marketing', 'Marketing'),
        ('development', 'Development'),
        ('sales', 'Sales'),
    ]
    name = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Marketing")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name')
        ]


class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name='tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        constraints = [
            models.UniqueConstraint(fields=['title', 'created_at'], name='unique_title_per_day'),
        ]

    def __str__(self):
        return self.title


class SubTask(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    task = models.ForeignKey(
        'Task',                 # Ссылается на основную задачу
        on_delete=models.CASCADE,  # Если Task удалится — удаляются и все SubTask
        related_name='subtasks'    # Можно будет получить все подзадачи через task.subtasks.all()
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        verbose_name_plural = 'SubTasks'
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_subtask_title')
        ]

    def __str__(self):
        return f"{self.title} (для задачи: {self.task.title})"




