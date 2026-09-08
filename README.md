# Employee Task Tracker

Микросервисный трекер задач для сотрудников.

## Архитектура

- **auth-service** — авторизация (JWT), пользователи
- **task-service** — задачи, проекты, сотрудники
- **notification-service** — уведомления (email)
- **frontend** — Vue 3 + Vite + Pinia

## Запуск

```bash
docker-compose up --build -d
```

Демо-доступ
Логин: demo

Пароль: demo12345

API
Сервис	Порт	Описание
auth-service	8002	Регистрация, логин, пользователи
task-service	8003	Задачи, проекты, сотрудники
notification-service	8004	Уведомления
Эндпоинты
auth-service
POST /api/auth/register/ — регистрация

POST /api/auth/login/ — логин (JWT)

GET /api/auth/users/ — список пользователей

task-service
GET /api/employees/ — список сотрудников

GET /api/employees/busy/ — занятые сотрудники

GET /api/tasks/ — список задач

GET /api/tasks/important/ — важные задачи

POST /api/tasks/ — создание задачи

notification-service
POST /api/notifications/send/ — отправка уведомления

Технологии
Python 3.11

Django + DRF

PostgreSQL

Redis + Celery

Docker + Docker Compose

Vue 3 + Vite + Pinia