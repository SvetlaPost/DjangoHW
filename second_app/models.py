from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

#user = User(
#    username="NEWUniqueUser",
#    email="newunique.email@gmail.com",
#    first_name="Unique2",
#    last_name="User2",
#)
#user.set_password("as-0dG<y0S8^d7fgtS<78")
#
#user.save()

class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Category(models.Model):
    STATUS_CHOICES = [
        ('marketing', 'Marketing'),
        ('development', 'Development'),
        ('sales', 'Sales'),
    ]
    name = models.CharField(max_length=20, default="Marketing")
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    objects = CategoryManager()  # фильтр удалённых
    all_objects = models.Manager()  # все записи, включая удалённые

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

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
    day_of_week = models.CharField(max_length=20, default='Monday')

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
        'Task',
        on_delete=models.CASCADE,
        related_name='subtasks'
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




