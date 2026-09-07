from rest_framework import serializers

from .models import Employee, Project, Task


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'position', 'email', 'hired_at']
        read_only_fields = ['hired_at']

    def validate_email(self, value):
        if Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError("Сотрудник с таким email уже существует.")
        return value


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['created_at']


class TaskSerializer(serializers.ModelSerializer):
    assignee_name = serializers.CharField(source='assignee.full_name', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'parent_task',
            'assignee', 'assignee_name', 'due_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_due_date(self, value):
        if value < self.context['request'].user.date_joined.date():
            raise serializers.ValidationError("Срок задачи не может быть в прошлом.")
        return value
