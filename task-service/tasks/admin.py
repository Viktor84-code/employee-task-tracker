from django.contrib import admin

from .models import Employee, Project, Task


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'email', 'hired_at']
    search_fields = ['full_name', 'position', 'email']
    list_filter = ['position']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'assignee', 'due_date', 'created_at']
    list_filter = ['status']
    search_fields = ['title', 'description']
    list_select_related = ['assignee']