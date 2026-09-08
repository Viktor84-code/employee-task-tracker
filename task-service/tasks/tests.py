from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Employee, Project, Task
from .serializers import EmployeeSerializer, ProjectSerializer, TaskSerializer
from .tasks import notify_task_created, notify_task_status_changed

User = get_user_model()


class EmployeeModelTest(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(
            full_name='Иван Иванов',
            position='Разработчик',
            email='ivan@example.com',
        )

    def test_create_employee(self):
        self.assertEqual(self.employee.full_name, 'Иван Иванов')
        self.assertEqual(self.employee.position, 'Разработчик')
        self.assertEqual(self.employee.email, 'ivan@example.com')
        self.assertIsNotNone(self.employee.hired_at)

    def test_str(self):
        self.assertEqual(str(self.employee), 'Иван Иванов')

    def test_email_unique(self):
        with self.assertRaises(Exception):
            Employee.objects.create(
                full_name='Другой Иван',
                position='Тестировщик',
                email='ivan@example.com',
            )

    def test_required_fields(self):
        with self.assertRaises(Exception):
            Employee.objects.create(full_name=None, email='x@example.com')

    def test_auto_now_add_hired_at(self):
        Employee.objects.create(
            full_name='Пётр Петров',
            position='Аналитик',
            email='petr@example.com',
        )
        self.assertTrue(Employee.objects.filter(full_name='Пётр Петров').exists())


class ProjectModelTest(TestCase):

    def setUp(self):
        self.project = Project.objects.create(
            name='Проект Альфа',
            description='Основной проект',
        )

    def test_create_project(self):
        self.assertEqual(self.project.name, 'Проект Альфа')
        self.assertEqual(self.project.description, 'Основной проект')
        self.assertIsNotNone(self.project.created_at)

    def test_str(self):
        self.assertEqual(str(self.project), 'Проект Альфа')

    def test_description_blank_default(self):
        project = Project.objects.create(name='Без описания')
        self.assertEqual(project.description, '')

    def test_auto_now_add_created_at(self):
        Project.objects.create(name='Ещё проект')
        self.assertTrue(Project.objects.filter(name='Ещё проект').exists())


class TaskModelTest(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(
            full_name='Иван Иванов',
            position='Разработчик',
            email='ivan@example.com',
        )
        self.task = Task.objects.create(
            title='Задача 1',
            description='Описание',
            assignee=self.employee,
            due_date=date.today() + timedelta(days=1),
        )

    def test_create_task(self):
        self.assertEqual(self.task.title, 'Задача 1')
        self.assertEqual(self.task.status, 'new')
        self.assertEqual(self.task.assignee, self.employee)
        self.assertIsNotNone(self.task.created_at)
        self.assertIsNotNone(self.task.updated_at)

    def test_str(self):
        self.assertEqual(str(self.task), 'Задача 1')

    def test_default_status(self):
        task = Task.objects.create(
            title='Новая задача',
            due_date=date.today() + timedelta(days=1),
        )
        self.assertEqual(task.status, 'new')

    def test_status_choices(self):
        for choice, _label in Task.STATUS_CHOICES:
            task = Task.objects.create(
                title=f'Задача {choice}',
                status=choice,
                due_date=date.today() + timedelta(days=1),
            )
            self.assertEqual(task.status, choice)

    def test_invalid_status_rejected_by_serializer(self):
        from .serializers import TaskSerializer
        mock_user = type(
            'U',
            (),
            {'date_joined': self.task.created_at},
        )
        serializer = TaskSerializer(
            data={
                'title': 'Невалидная задача',
                'status': 'invalid_status',
                'due_date': date.today() + timedelta(days=1),
            },
            context={'request': type('R', (), {'user': mock_user})()},
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('status', serializer.errors)

    def test_parent_task(self):
        parent = Task.objects.create(
            title='Родительская задача',
            due_date=date.today() + timedelta(days=2),
        )
        subtask = Task.objects.create(
            title='Подзадача',
            parent_task=parent,
            due_date=date.today() + timedelta(days=3),
        )
        self.assertEqual(subtask.parent_task, parent)
        self.assertIn(subtask, parent.subtasks.all())

    def test_subtask_can_be_unset(self):
        parent = Task.objects.create(
            title='Родительская задача',
            due_date=date.today() + timedelta(days=2),
        )
        subtask = Task.objects.create(
            title='Подзадача',
            parent_task=parent,
            due_date=date.today() + timedelta(days=3),
        )
        subtask.parent_task = None
        subtask.save()
        self.assertIsNone(subtask.parent_task)

    def test_assignee_can_be_unset(self):
        self.task.assignee = None
        self.task.save()
        self.task.refresh_from_db()
        self.assertIsNone(self.task.assignee)

    def test_delete_employee_sets_assignee_null(self):
        employee = Employee.objects.create(
            full_name='Временный',
            position='Стажёр',
            email='temp@example.com',
        )
        task = Task.objects.create(
            title='Задача стажёра',
            assignee=employee,
            due_date=date.today() + timedelta(days=1),
        )
        employee.delete()
        task.refresh_from_db()
        self.assertIsNone(task.assignee)

    def test_delete_parent_keeps_subtask(self):
        parent = Task.objects.create(
            title='Родительская',
            due_date=date.today() + timedelta(days=2),
        )
        subtask = Task.objects.create(
            title='Подзадача',
            parent_task=parent,
            due_date=date.today() + timedelta(days=3),
        )
        parent.delete()
        subtask.refresh_from_db()
        self.assertIsNone(subtask.parent_task)

    def test_related_name_tasks(self):
        self.assertEqual(self.employee.tasks.count(), 1)


class EmployeeSerializerTest(TestCase):

    def setUp(self):
        self.employee = Employee.objects.create(
            full_name='Иван Иванов',
            position='Разработчик',
            email='ivan@example.com',
        )

    def test_serializer_fields(self):
        serializer = EmployeeSerializer(self.employee)
        data = serializer.data
        self.assertEqual(
            set(data.keys()), {'id', 'full_name', 'position', 'email', 'hired_at'}
        )

    def test_serializer_valid_data(self):
        serializer = EmployeeSerializer(data={
            'full_name': 'Пётр Петров',
            'position': 'Аналитик',
            'email': 'petr@example.com',
        })
        self.assertTrue(serializer.is_valid())

    def test_serializer_duplicate_email(self):
        serializer = EmployeeSerializer(data={
            'full_name': 'Другой',
            'position': 'Тестировщик',
            'email': 'ivan@example.com',
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_serializer_missing_required_fields(self):
        serializer = EmployeeSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn('full_name', serializer.errors)
        self.assertIn('email', serializer.errors)

    def test_hired_at_read_only(self):
        serializer = EmployeeSerializer(data={
            'full_name': 'Новый',
            'position': 'Должность',
            'email': 'new@example.com',
            'hired_at': '2020-01-01',
        })
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('hired_at', serializer.validated_data)


class ProjectSerializerTest(TestCase):

    def setUp(self):
        self.project = Project.objects.create(name='Проект', description='Описание')

    def test_serializer_fields(self):
        serializer = ProjectSerializer(self.project)
        data = serializer.data
        self.assertEqual(
            set(data.keys()), {'id', 'name', 'description', 'created_at'}
        )

    def test_serializer_valid_data(self):
        serializer = ProjectSerializer(data={'name': 'Новый', 'description': ''})
        self.assertTrue(serializer.is_valid())

    def test_serializer_missing_name(self):
        serializer = ProjectSerializer(data={'description': 'без имени'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_created_at_read_only(self):
        serializer = ProjectSerializer(data={
            'name': 'С created_at',
            'created_at': '2020-01-01T00:00:00Z',
        })
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('created_at', serializer.validated_data)


class TaskSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
        )
        self.employee = Employee.objects.create(
            full_name='Иван Иванов',
            position='Разработчик',
            email='ivan@example.com',
        )
        self.task = Task.objects.create(
            title='Задача',
            description='Описание',
            assignee=self.employee,
            due_date=date.today() + timedelta(days=5),
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_serializer_fields(self):
        serializer = TaskSerializer(self.task)
        data = serializer.data
        self.assertEqual(
            set(data.keys()),
            {
                'id', 'title', 'description', 'status', 'parent_task',
                'assignee', 'assignee_name', 'due_date', 'created_at', 'updated_at'
            }
        )

    def test_assignee_name(self):
        serializer = TaskSerializer(self.task)
        self.assertEqual(serializer.data['assignee_name'], 'Иван Иванов')

    def test_assignee_name_none(self):
        task = Task.objects.create(
            title='Без исполнителя',
            due_date=date.today() + timedelta(days=5),
        )
        serializer = TaskSerializer(task)
        self.assertIsNone(serializer.data.get('assignee_name'))

    def test_valid_task_data(self):
        serializer = TaskSerializer(
            data={
                'title': 'Новая',
                'due_date': date.today() + timedelta(days=10),
                'assignee': self.employee.id,
            },
            context={'request': type('R', (), {'user': self.user})()},
        )
        self.assertTrue(serializer.is_valid())

    def test_due_date_in_past_invalid(self):
        serializer = TaskSerializer(
            data={
                'title': 'Просрочено',
                'due_date': date.today() - timedelta(days=1),
            },
            context={'request': type('R', (), {'user': self.user})()},
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('due_date', serializer.errors)

    def test_missing_title(self):
        serializer = TaskSerializer(
            data={'due_date': date.today() + timedelta(days=1)},
            context={'request': type('R', (), {'user': self.user})()},
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_missing_due_date(self):
        serializer = TaskSerializer(
            data={'title': 'Без срока'},
            context={'request': type('R', (), {'user': self.user})()},
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('due_date', serializer.errors)

    def test_created_at_updated_at_read_only(self):
        serializer = TaskSerializer(
            data={
                'title': 'Задача',
                'due_date': date.today() + timedelta(days=1),
                'created_at': '2020-01-01T00:00:00Z',
                'updated_at': '2020-01-01T00:00:00Z',
            },
            context={'request': type('R', (), {'user': self.user})()},
        )
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('created_at', serializer.validated_data)
        self.assertNotIn('updated_at', serializer.validated_data)


class EmployeeAPITest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
        )
        self.client = APIClient()
        self.employee = Employee.objects.create(
            full_name='Иван Иванов',
            position='Разработчик',
            email='ivan@example.com',
        )
        self.url = '/api/employees/'

    def test_create_employee_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {
            'full_name': 'Пётр Петров',
            'position': 'Аналитик',
            'email': 'petr@example.com',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)

    def test_list_employees_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_employees_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_employee(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.url}{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'ivan@example.com')

    def test_retrieve_nonexistent(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.url}999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_employee(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'{self.url}{self.employee.id}/', {
            'position': 'Старший разработчик',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.position, 'Старший разработчик')

    def test_delete_employee(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'{self.url}{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)

    def test_create_duplicate_email(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {
            'full_name': 'Другой',
            'position': 'Тестировщик',
            'email': 'ivan@example.com',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_employee_id_is_int(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.url}{self.employee.id}/')
        self.assertIsInstance(response.data['id'], int)


class ProjectAPITest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
        )
        self.client = APIClient()
        self.project = Project.objects.create(name='Проект', description='Описание')
        self.url = '/api/projects/'

    def test_create_project_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {
            'name': 'Новый проект',
            'description': 'test',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_list_projects_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_projects_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_project(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'{self.url}{self.project.id}/', {
            'description': 'Обновлённое описание',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, 'Обновлённое описание')

    def test_create_project_without_name(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {
            'description': 'без имени',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TaskAPITest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
        )
        self.client = APIClient()
        self.employee = Employee.objects.create(
            full_name='Иван Иванов',
            position='Разработчик',
            email='ivan@example.com',
        )
        self.task = Task.objects.create(
            title='Задача',
            assignee=self.employee,
            due_date=date.today() + timedelta(days=5),
        )
        self.url = '/api/tasks/'

    def test_create_task_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {
            'title': 'Новая задача',
            'due_date': date.today() + timedelta(days=10),
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_create_task_with_past_due_date(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {
            'title': 'Просроченная',
            'due_date': date.today() - timedelta(days=1),
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_task_with_invalid_status(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {
            'title': 'Невалидный статус',
            'status': 'invalid_status',
            'due_date': date.today() + timedelta(days=1),
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_tasks_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_tasks_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_task(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.url}{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Задача')

    def test_update_task_status(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'{self.url}{self.task.id}/', {
            'status': 'in_progress',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'in_progress')

    def test_update_task_title(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'{self.url}{self.task.id}/', {
            'title': 'Обновлённая задача',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Обновлённая задача')

    def test_delete_task(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'{self.url}{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_assignee_name_in_response(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.url}{self.task.id}/')
        self.assertEqual(response.data['assignee_name'], 'Иван Иванов')


class BusyEmployeesTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.busy = Employee.objects.create(
            full_name='Занятый',
            position='Разработчик',
            email='busy@example.com',
        )
        self.idle = Employee.objects.create(
            full_name='Свободный',
            position='Дизайнер',
            email='idle@example.com',
        )
        for status_ in ('new', 'in_progress', 'done'):
            Task.objects.create(
                title=f'Задача {status_}',
                assignee=self.busy,
                status=status_,
                due_date=date.today() + timedelta(days=5),
            )
        Task.objects.create(
            title='Одна задача',
            assignee=self.idle,
            status='in_progress',
            due_date=date.today() + timedelta(days=5),
        )

    def test_busy_returns_ordered_employees(self):
        response = self.client.get('/api/employees/busy/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['full_name'], 'Занятый')
        self.assertEqual(response.data[1]['full_name'], 'Свободный')

    def test_busy_requires_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/employees/busy/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_busy_with_no_employees(self):
        Employee.objects.all().delete()
        response = self.client.get('/api/employees/busy/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_busy_counts_only_active_tasks(self):
        response = self.client.get('/api/employees/busy/')
        busy_data = next(e for e in response.data if e['full_name'] == 'Занятый')
        self.assertNotIn('active_tasks_count', busy_data)


class ImportantTasksTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.loaded = Employee.objects.create(
            full_name='Перегруженный',
            position='Разработчик',
            email='loaded@example.com',
        )
        self.free = Employee.objects.create(
            full_name='Свободный сотрудник',
            position='Тестировщик',
            email='free@example.com',
        )

    def test_important_empty_when_no_tasks(self):
        response = self.client.get('/api/tasks/important/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_important_returns_new_parent_with_in_progress_subtask(self):
        parent = Task.objects.create(
            title='Родительская',
            status='new',
            due_date=date.today() + timedelta(days=5),
        )
        Task.objects.create(
            title='Подзадача',
            parent_task=parent,
            status='in_progress',
            due_date=date.today() + timedelta(days=5),
        )
        response = self.client.get('/api/tasks/important/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['task'], 'Родительская')

    def test_important_excludes_done_parent(self):
        parent = Task.objects.create(
            title='Завершённая',
            status='done',
            due_date=date.today() + timedelta(days=5),
        )
        Task.objects.create(
            title='Подзадача',
            parent_task=parent,
            status='in_progress',
            due_date=date.today() + timedelta(days=5),
        )
        response = self.client.get('/api/tasks/important/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_important_excludes_parent_with_done_subtask(self):
        parent = Task.objects.create(
            title='Родительская',
            status='new',
            due_date=date.today() + timedelta(days=5),
        )
        Task.objects.create(
            title='Подзадача',
            parent_task=parent,
            status='done',
            due_date=date.today() + timedelta(days=5),
        )
        response = self.client.get('/api/tasks/important/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_important_requires_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/tasks/important/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_important_no_duplicates(self):
        parent = Task.objects.create(
            title='Родительская',
            status='new',
            due_date=date.today() + timedelta(days=5),
        )
        Task.objects.create(
            title='Подзадача 1',
            parent_task=parent,
            status='in_progress',
            assignee=self.free,
            due_date=date.today() + timedelta(days=5),
        )
        Task.objects.create(
            title='Подзадача 2',
            parent_task=parent,
            status='in_progress',
            assignee=self.free,
            due_date=date.today() + timedelta(days=5),
        )
        response = self.client.get('/api/tasks/important/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_important_includes_least_loaded_candidate(self):
        parent = Task.objects.create(
            title='Родительская',
            status='new',
            due_date=date.today() + timedelta(days=5),
        )
        Task.objects.create(
            title='Подзадача',
            parent_task=parent,
            status='in_progress',
            due_date=date.today() + timedelta(days=5),
        )
        response = self.client.get('/api/tasks/important/')
        employees = response.data[0]['employees']
        self.assertIn('Свободный сотрудник', employees)

    def test_important_includes_nested_parent_assignee_when_underloaded(self):
        grandparent = Task.objects.create(
            title='Родительская задача',
            status='new',
            assignee=self.free,
            due_date=date.today() + timedelta(days=5),
        )
        important = Task.objects.create(
            title='Важная подзадача',
            status='new',
            parent_task=grandparent,
            due_date=date.today() + timedelta(days=5),
        )
        Task.objects.create(
            title='Подзадача',
            parent_task=important,
            status='in_progress',
            due_date=date.today() + timedelta(days=5),
        )
        response = self.client.get('/api/tasks/important/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        employees = response.data[0]['employees']
        self.assertIn('Свободный сотрудник', employees)

    def test_important_excludes_loaded_parent_assignee(self):
        for i in range(3):
            Task.objects.create(
                title=f'Нагрузочная {i}',
                assignee=self.loaded,
                status='in_progress',
                due_date=date.today() + timedelta(days=5),
            )
        grandparent = Task.objects.create(
            title='Родительская задача',
            status='new',
            assignee=self.loaded,
            due_date=date.today() + timedelta(days=5),
        )
        important = Task.objects.create(
            title='Важная подзадача',
            status='new',
            parent_task=grandparent,
            due_date=date.today() + timedelta(days=5),
        )
        Task.objects.create(
            title='Подзадача',
            parent_task=important,
            status='in_progress',
            due_date=date.today() + timedelta(days=5),
        )
        response = self.client.get('/api/tasks/important/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        employees = response.data[0]['employees']
        self.assertNotIn('Перегруженный', employees)
        self.assertIn('Свободный сотрудник', employees)

    def test_important_no_employees_registered(self):
        Employee.objects.all().delete()
        parent = Task.objects.create(
            title='Родительская',
            status='new',
            due_date=date.today() + timedelta(days=5),
        )
        Task.objects.create(
            title='Подзадача',
            parent_task=parent,
            status='in_progress',
            due_date=date.today() + timedelta(days=5),
        )
        response = self.client.get('/api/tasks/important/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['employees'], [])


class CeleryTasksTest(TestCase):

    def test_notify_task_created_requires_email(self):
        with self.assertRaises(ValueError):
            notify_task_created(
                task_id=1,
                assignee_email=None,
                message='test message',
            )

    def test_notify_task_created_empty_email(self):
        with self.assertRaises(ValueError):
            notify_task_created(
                task_id=1,
                assignee_email='',
                message='test message',
            )

    def test_notify_task_created_sends_email(self):
        notify_task_created(
            task_id=1,
            assignee_email='user@example.com',
            message='Новая задача создана',
        )
        self.assertEqual(len(mail.outbox), 1)
        sent = mail.outbox[0]
        self.assertEqual(sent.subject, 'Новая задача')
        self.assertEqual(sent.to, ['user@example.com'])
        self.assertEqual(sent.body, 'Новая задача создана')

    def test_notify_task_status_changed_requires_email(self):
        with self.assertRaises(ValueError):
            notify_task_status_changed(
                task_id=1,
                creator_email=None,
                message='status changed',
            )

    def test_notify_task_status_changed_empty_email(self):
        with self.assertRaises(ValueError):
            notify_task_status_changed(
                task_id=1,
                creator_email='',
                message='status changed',
            )

    def test_notify_task_status_changed_sends_email(self):
        notify_task_status_changed(
            task_id=1,
            creator_email='creator@example.com',
            message='Статус задачи обновлён',
        )
        self.assertEqual(len(mail.outbox), 1)
        sent = mail.outbox[0]
        self.assertEqual(sent.subject, 'Статус задачи изменён')
        self.assertEqual(sent.to, ['creator@example.com'])
        self.assertEqual(sent.body, 'Статус задачи обновлён')
