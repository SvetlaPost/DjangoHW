
from django.contrib import admin
from .models import Task, SubTask, Category


#@admin.register(Task)
#class TaskAdmin(admin.ModelAdmin):
#    list_display = ('title', 'status', 'deadline', 'created_at')
#    search_fields = ('title', 'description')
#    list_filter = ('status', 'deadline', 'created_at')
#    date_hierarchy = 'deadline'
#
#
#@admin.register(SubTask)
#class SubTaskAdmin(admin.ModelAdmin):
#    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
#    search_fields = ('title', 'description')
#    list_filter = ('status', 'deadline', 'created_at', 'task')
#    date_hierarchy = 'deadline'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    show_change_link = True

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['short_title', 'status', 'deadline']
    inlines = [SubTaskInline]
    search_fields = ['title', 'description']

    def short_title(self, obj):
        return (obj.title[:15] + '...') if len(obj.title) > 15 else obj.title

    short_title.short_description = "Title"

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'deadline', 'short_task']
    search_fields = ['title', 'description', 'task__title']
    actions = ["mark_as_done"]

    def short_task(self, obj):
        full_title = obj.task.title
        return (full_title[:15] + '...') if len(full_title) > 15 else full_title

    short_task.short_description = "Task"

    @admin.action(description="Mark selected tasks as done")
    def mark_as_done(self, request, queryset):
        updated = queryset.update(status="done")
        self.message_user(request, f"Updated {updated} tasks as Done.")


