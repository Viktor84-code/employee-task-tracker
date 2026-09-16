from django.db.models import Count, Q
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Employee, Project, Task
from .serializers import (
    EmployeeSerializer,
    EmployeeBusySerializer,
    ProjectSerializer,
    TaskSerializer,
)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def busy(self, request):
        employees = Employee.objects.annotate(
            active_tasks_count=Count(
                'tasks',
                filter=Q(tasks__status__in=['new', 'in_progress'])
            )
        ).order_by('-active_tasks_count')

        serializer = EmployeeBusySerializer(employees, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def workload(self, request):
        """
        Внутренний API: количество активных задач на каждого сотрудника.
        """
        employees = Employee.objects.annotate(
            active_tasks_count=Count(
                'tasks',
                filter=Q(tasks__status__in=['new', 'in_progress'])
            )
        )

        return Response([
            {'employee_id': emp.id, 'active_tasks_count': emp.active_tasks_count}
            for emp in employees
        ])


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def important(self, request):
        important_tasks = Task.objects.filter(
            status='new',
            subtasks__status='in_progress'
        ).distinct()

        employees_with_load = list(
            Employee.objects.annotate(
                active_tasks_count=Count(
                    'tasks',
                    filter=Q(tasks__status__in=['new', 'in_progress'])
                )
            ).order_by('active_tasks_count')
        )

        least_loaded = employees_with_load[0] if employees_with_load else None
        min_load = least_loaded.active_tasks_count if least_loaded else 0

        result = []
        for task in important_tasks:
            candidates = []

            task_assignee = task.assignee
            if task_assignee:
                assignee_load = task_assignee.tasks.filter(
                    status__in=['new', 'in_progress']
                ).count()
                if assignee_load <= min_load + 2:
                    candidates.append(task_assignee.full_name)

            if least_loaded:
                candidates.append(least_loaded.full_name)

            result.append({
                'task': task.title,
                'due_date': task.due_date,
                'employees': list(set(candidates)),
            })

        return Response(result)
