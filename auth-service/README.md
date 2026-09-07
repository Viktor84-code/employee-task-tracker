# Auth Service

Микросервис авторизации и управления пользователями.

## Технологии

- Django 5.2
- DRF
- JWT (SimpleJWT)
- PostgreSQL

## Запуск в Docker

```bash
docker-compose up -d auth-service
```

API
POST /api/auth/register/ — регистрация

POST /api/auth/login/ — логин (JWT)

GET /api/auth/users/ — список пользователей# Task Service

Микросервис управления задач и сотрудниками.

## Технологии

- Django 5.2
# Notification Service

Микросервис уведомлений (email).

## Технологии

- Django 5.2
- DRF
- Celery
- Redis

## Запуск в Docker

```bash
docker-compose up -d notification-service
```

API
Уведомления через Celery (email)