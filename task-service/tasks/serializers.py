from datetime import date

from rest_framework import serializers

from .models import Employee, Project, Task


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'position', 'email', 'hired_at']
        read_only_fields = ['hired_at']

    def validate_email(self, value):
        queryset = Employee.objects.filter(email=value)
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
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
        if value < date.today():
            raise serializers.ValidationError("Срок задачи не может быть в прошлом.")
        return value


class EmployeeBusySerializer(serializers.ModelSerializer):
    active_tasks_count = serializers.IntegerField(read_only=True)
    active_tasks = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id', 'full_name', 'position', 'email', 'hired_at',
            'active_tasks_count', 'active_tasks',
        ]

    def get_active_tasks(self, obj):
        tasks = obj.tasks.filter(status__in=['new', 'in_progress'])
        return [
            {
                'id': t.id,
                'title': t.title,
                'status': t.status,
                'due_date': t.due_date,
            }
            for t in tasks
        ]
