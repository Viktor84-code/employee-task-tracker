from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='employee',
        )

    def test_create_user(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.role, 'employee')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertFalse(self.user.is_staff)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_default_role_is_employee(self):
        user = User.objects.create_user(
            username='nodefault',
            email='nodefault@example.com',
            password='testpass123',
        )
        self.assertEqual(user.role, 'employee')

    def test_role_choices(self):
        for role in ('admin', 'manager', 'employee'):
            user = User.objects.create_user(
                username=f'user_{role}',
                email=f'{role}@example.com',
                password='testpass123',
                role=role,
            )
            self.assertEqual(user.role, role)

    def test_str(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_email_unique_constraint(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser2',
                email='test@example.com',
                password='testpass123',
            )

    def test_username_unique_constraint(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser',
                email='other@example.com',
                password='testpass123',
            )

    def test_user_without_email(self):
        user = User.objects.create_user(
            username='noemail',
            password='testpass123',
        )
        self.assertEqual(user.email, '')

    def test_update_user_role(self):
        self.user.role = 'manager'
        self.user.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, 'manager')

    def test_password_is_hashed(self):
        self.assertNotEqual(self.user.password, 'testpass123')

    def test_check_wrong_password(self):
        self.assertFalse(self.user.check_password('wrongpassword'))


class UserSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='manager',
        )

    def test_user_serializer_fields(self):
        serializer = UserSerializer(self.user)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'id', 'username', 'email', 'role'})
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['role'], 'manager')

    def test_user_serializer_read_only_id(self):
        serializer = UserSerializer(self.user)
        self.assertIn('id', serializer.data)

    def test_register_serializer_valid(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'validpass123',
            'role': 'employee',
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_register_serializer_create(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'validpass123',
            'role': 'employee',
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'new@example.com')
        self.assertEqual(user.role, 'employee')
        self.assertTrue(user.check_password('validpass123'))

    def test_register_serializer_short_password(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'short',
            'role': 'employee',
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_register_serializer_duplicate_email(self):
        data = {
            'username': 'another',
            'email': 'test@example.com',
            'password': 'validpass123',
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_register_serializer_missing_fields(self):
        serializer = RegisterSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
        self.assertIn('email', serializer.errors)
        self.assertIn('password', serializer.errors)

    def test_register_serializer_default_role(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'validpass123',
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.role, 'employee')


class RegisterViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/register/'
        self.valid_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'validpass123',
            'role': 'employee',
        }

    def test_register_success(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'newuser')

    def test_register_duplicate_email(self):
        User.objects.create_user(
            username='existing',
            email='new@example.com',
            password='testpass123',
        )
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_short_password(self):
        data = self.valid_data.copy()
        data['password'] = 'short'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_missing_fields(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_no_auth_required(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_returns_user_fields(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(response.data.keys()), {'username', 'email', 'role'})
        self.assertNotIn('password', response.data)


class UserListViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/api/auth/users/'
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
        )

    def test_list_users_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_users_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_users_multiple(self):
        User.objects.create_user(
            username='user2', email='user2@example.com', password='testpass123'
        )
        User.objects.create_user(
            username='user3', email='user3@example.com', password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_users_returns_correct_fields(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_data = response.data[0]
        self.assertIn('id', user_data)
        self.assertIn('username', user_data)
        self.assertIn('email', user_data)
        self.assertIn('role', user_data)
        self.assertNotIn('password', user_data)

    def test_list_users_does_not_expose_password(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        for user_data in response.data:
            self.assertNotIn('password', user_data)
            self.assertNotIn('last_login', user_data)


class JWTAuthTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
        )

    def test_obtain_token(self):
        response = self.client.post(
            '/api/auth/login/',
            {'username': 'testuser', 'password': 'testpass123'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_obtain_token_wrong_password(self):
        response = self.client.post(
            '/api/auth/login/',
            {'username': 'testuser', 'password': 'wrongpassword'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_obtain_token_nonexistent_user(self):
        response = self.client.post(
            '/api/auth/login/',
            {'username': 'nobody', 'password': 'testpass123'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        login_response = self.client.post(
            '/api/auth/login/',
            {'username': 'testuser', 'password': 'testpass123'},
            format='json',
        )
        refresh_token = login_response.data['refresh']
        response = self.client.post(
            '/api/auth/refresh/',
            {'refresh': refresh_token},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_refresh_token_invalid(self):
        response = self.client.post(
            '/api/auth/refresh/',
            {'refresh': 'invalid-token'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_endpoint_with_token(self):
        login_response = self.client.post(
            '/api/auth/login/',
            {'username': 'testuser', 'password': 'testpass123'},
            format='json',
        )
        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/auth/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_protected_endpoint_without_token(self):
        response = self.client.get('/api/auth/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_then_login(self):
        self.client.post(
            '/api/auth/register/',
            {
                'username': 'brandnew',
                'email': 'brandnew@example.com',
                'password': 'securepass123',
            },
            format='json',
        )
        response = self.client.post(
            '/api/auth/login/',
            {'username': 'brandnew', 'password': 'securepass123'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
