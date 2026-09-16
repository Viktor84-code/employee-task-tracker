# Employee Task Tracker

Микросервисный трекер задач для сотрудников.

## Содержание

- [Архитектура](#архитектура)
- [Технологии](#технологии)
- [Структура проекта](#структура-проекта)
- [Запуск локально](#запуск-локально)
- [Переменные окружения](#переменные-окружения)
- [API](#api)
  - [Авторизация](#авторизация)
  - [auth-service](#auth-service)
  - [task-service](#task-service)
  - [notification-service](#notification-service)
- [Модели данных](#модели-данных)
- [Тесты](#тесты)
- [CI/CD](#cicd)
- [Прод-доступ](#прод-доступ)

## Архитектура

- **auth-service** — авторизация (JWT), пользователи
- **task-service** — задачи, сотрудники, проекты
- **notification-service** — уведомления (email)
- **frontend** — Vue 3 + Vite + Pinia
- **postgres** (×3) — отдельная БД на каждый сервис
- **redis** — кэш + брокер Celery

## Технологии

- Python 3.11, Django + DRF
- PostgreSQL 16
- Redis 7 + Celery
- Docker + Docker Compose
- Vue 3 + Vite + Pinia
- GitHub Actions (CI/CD)

## Структура проекта

```
employee-task-tracker/
├── auth-service/             # авторизация, JWT, пользователи
│   ├── config/
│   ├── users/
│   ├── entrypoint.sh
│   └── Dockerfile
├── task-service/             # задачи, сотрудники, проекты
│   ├── config/
│   ├── tasks/
│   ├── users/
│   ├── entrypoint.sh
│   └── Dockerfile
├── notification-service/     # уведомления, Celery worker
│   ├── config/
│   ├── notifications/
│   └── Dockerfile
├── frontend/                 # Vue 3 SPA
├── .github/workflows/        # CI/CD
├── docker-compose.yml
├── .env.example
└── README.md
```

## Запуск локально

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Viktor84-code/employee-task-tracker.git
cd employee-task-tracker
```

### 2. Создать `.env`

```bash
cp .env.example .env
```

Отредактировать `.env`, указав свои значения (см. [Переменные окружения](#переменные-окружения)).

### 3. Поднять стек

```bash
docker-compose up --build -d
```

### 4. Проверить

```bash
docker-compose ps
```

Все сервисы должны быть в состоянии `Up`.

### 5. Доступы

- Frontend: http://localhost:5173/
- Swagger (auth): http://localhost:8002/api/docs/
- Swagger (task): http://localhost:8003/api/docs/
- Swagger (notification): http://localhost:8004/api/docs/
- Django Admin (task): http://localhost:8003/admin/

**Демо-доступ:** `demo / demo12345`

## Переменные окружения

Файл `.env` в корне проекта:

| Переменная | Описание | Пример |
|---|---|---|
| `SECRET_KEY` | Django SECRET_KEY | `django-insecure-...` |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL | `strongpassword` |
| `DJANGO_SUPERUSER_USERNAME` | Логин суперюзера | `admin` |
| `DJANGO_SUPERUSER_EMAIL` | Email суперюзера | `admin@example.com` |
| `DJANGO_SUPERUSER_PASSWORD` | Пароль суперюзера | `strongpassword` |

> ⚠️ В продакшене `.env` **не коммитится** в git. Переменные хранятся в GitHub Secrets и подставляются автоматически при деплое.

## API

Base URL:

- auth-service: `http://localhost:8002`
- task-service: `http://localhost:8003`
- notification-service: `http://localhost:8004`

### Авторизация

Все эндпоинты (кроме `/api/auth/register/` и `/api/auth/login/`) требуют JWT:

```
Authorization: Bearer <access_token>
```

### auth-service

| Метод | URL | Описание |
|---|---|---|
| POST | `/api/auth/register/` | Регистрация нового пользователя |
| POST | `/api/auth/login/` | Получить access + refresh токены |
| POST | `/api/auth/refresh/` | Обновить access-токен |
| GET | `/api/auth/users/` | Список пользователей |

**Пример: логин**

```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "demo",
  "password": "demo12345"
}
```

**Ответ:**

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### task-service

#### CRUD: Сотрудники

| Метод | URL | Описание |
|---|---|---|
| GET | `/api/employees/` | Список сотрудников |
| POST | `/api/employees/` | Создать сотрудника |
| GET | `/api/employees/{id}/` | Получить сотрудника |
| PUT/PATCH | `/api/employees/{id}/` | Обновить сотрудника |
| DELETE | `/api/employees/{id}/` | Удалить сотрудника |

**Пример: создание**

```http
POST /api/employees/
Authorization: Bearer <token>

{
  "full_name": "Иван Иванов",
  "position": "Разработчик",
  "email": "ivan@example.com"
}
```

#### CRUD: Задачи

| Метод | URL | Описание |
|---|---|---|
| GET | `/api/tasks/` | Список задач |
| POST | `/api/tasks/` | Создать задачу |
| GET | `/api/tasks/{id}/` | Получить задачу |
| PUT/PATCH | `/api/tasks/{id}/` | Обновить задачу |
| DELETE | `/api/tasks/{id}/` | Удалить задачу |

**Пример: создание**

```http
POST /api/tasks/
Authorization: Bearer <token>

{
  "title": "Написать отчёт",
  "description": "Квартальный отчёт по проекту",
  "status": "new",
  "assignee": 1,
  "due_date": "2026-12-31"
}
```

> `due_date` не может быть в прошлом.

#### CRUD: Проекты

| Метод | URL | Описание |
|---|---|---|
| GET | `/api/projects/` | Список проектов |
| POST | `/api/projects/` | Создать проект |
| GET | `/api/projects/{id}/` | Получить проект |
| PUT/PATCH | `/api/projects/{id}/` | Обновить проект |
| DELETE | `/api/projects/{id}/` | Удалить проект |

#### Спецэндпоинт: занятые сотрудники

**`GET /api/employees/busy/`**

Возвращает сотрудников, отсортированных по убыванию числа активных задач (`new` + `in_progress`), вместе со списком этих задач.

**Ответ:**

```json
[
  {
    "id": 1,
    "full_name": "Иван Иванов",
    "position": "Разработчик",
    "email": "ivan@example.com",
    "hired_at": "2026-01-15",
    "active_tasks_count": 3,
    "active_tasks": [
      {
        "id": 10,
        "title": "Написать отчёт",
        "status": "new",
        "due_date": "2026-12-31"
      },
      {
        "id": 11,
        "title": "Созвон с клиентом",
        "status": "in_progress",
        "due_date": "2026-10-15"
      }
    ]
  }
]
```

#### Спецэндпоинт: важные задачи

**`GET /api/tasks/important/`**

Возвращает задачи со статусом `new`, у которых есть хотя бы одна подзадача в статусе `in_progress`. Для каждой задачи подбираются кандидаты-исполнители:

1. **Исполнитель самой задачи** (`task.assignee`) — если его текущая нагрузка не превышает `min + 2` активных задач, где `min` — минимальная нагрузка среди всех сотрудников.
2. **Наименее загруженный сотрудник** — всегда в списке кандидатов.

**Ответ:**

```json
[
  {
    "task": "Подготовить релиз",
    "due_date": "2026-11-20",
    "employees": [
      "Иван Иванов",
      "Пётр Петров"
    ]
  }
]
```

### notification-service

| Метод | URL | Описание |
|---|---|---|
| POST | `/api/notifications/send/` | Отправить уведомление (Celery task) |

**Пример:**

```http
POST /api/notifications/send/
Authorization: Bearer <token>

{
  "recipient": "user@example.com",
  "subject": "Задача назначена",
  "message": "Вам назначена задача «Написать отчёт»"
}
```

## Модели данных

### Employee

| Поле | Тип | Описание |
|---|---|---|
| `id` | int | PK |
| `full_name` | str | ФИО |
| `position` | str | Должность |
| `email` | str | Email (уникальный) |
| `hired_at` | date | Дата найма (авто) |

### Task

| Поле | Тип | Описание |
|---|---|---|
| `id` | int | PK |
| `title` | str | Название |
| `description` | text | Описание |
| `status` | enum | `new` / `in_progress` / `done` |
| `parent_task` | FK → Task | Родительская задача (опц.) |
| `assignee` | FK → Employee | Исполнитель (опц.) |
| `due_date` | date | Срок |
| `created_at` | datetime | Авто |
| `updated_at` | datetime | Авто |

### Project

| Поле | Тип | Описание |
|---|---|---|
| `id` | int | PK |
| `name` | str | Название |
| `description` | text | Описание |
| `created_at` | datetime | Авто |

## Тесты

```bash
# auth-service
cd auth-service
python manage.py test --settings=config.test_settings

# task-service
cd ../task-service
python manage.py test --settings=config.test_settings

# notification-service
cd ../notification-service
python manage.py test --settings=config.test_settings
```

**Покрытие:**

- auth-service: 96%
- task-service: 97% (90 тестов)
- notification-service: 96%

**Линтер:**

```bash
flake8 .
```

## CI/CD

GitHub Actions (`.github/workflows/`):

- **`ci.yml`** — прогон тестов и flake8 на push и PR в `develop`
- **`deploy.yml`** — сборка Docker-образов и деплой на Yandex Cloud при push в `develop` или `feature/ci-cd`

**Как работает деплой:**

1. Прогон тестов
2. Сборка образов
3. SSH на VM → `git pull` → запись `.env` из GitHub Secrets → `docker-compose up --build -d`

## Прод-доступ

- **Frontend:** http://84.201.151.212:5173/
- **Django Admin:** http://84.201.151.212:8003/admin/
- **Swagger (auth):** http://84.201.151.212:8002/api/docs/
- **Swagger (task):** http://84.201.151.212:8003/api/docs/
- **Swagger (notification):** http://84.201.151.212:8004/api/docs/

**Демо-доступ:** `demo / demo12345`