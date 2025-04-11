from django.contrib import admin

from django.contrib import admin
from .models import Task, SubTask
from .models import Task, SubTask, Category  # не забудь импортировать Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'deadline', 'created_at')
    date_hierarchy = 'deadline'


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'deadline', 'created_at', 'task')
    date_hierarchy = 'deadline'

#ПРИМЕРЫ ЗАВЕДЕНИЯ ПРОЕКТОВ А АДМИН

# 1  admin.site.register(<Model>)
#class ModelAdmin(admin.ModelAdmin):
    ...

# admin.site.register(<Model>, ModelAdmin)


#@admin.register(<Model>)
#class ModelAdmin(admin.ModelAdmin):
 #   ...