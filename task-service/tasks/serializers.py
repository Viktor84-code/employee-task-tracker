from rest_framework import serializers

from .models import Employee, Project, Task


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'position', 'email', 'hired_at']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    assignee_name = serializers.CharField(source='assignee.full_name', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'parent_task',
            'assignee', 'assignee_name', 'due_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
