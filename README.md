# Employee Task Tracker

Микросервисный трекер задач для сотрудников.

## Архитектура

- **auth-service** — авторизация (JWT), пользователи
- **task-service** — задачи, сотрудники, проекты
- **notification-service** — уведомления (email)
- **frontend** — Vue 3 + Vite + Pinia

## Демо-доступ

- **Логин:** `demo`
- **Пароль:** `demo12345`

## Прод-доступ (Yandex Cloud)

- **Сайт:** http://84.201.151.212:5173/
- **Админка:** http://84.201.151.212:8003/admin/
- **Swagger:** http://84.201.151.212:8002/api/docs/

## Запуск локально

```bash
docker-compose up --build -d
```

API
Сервис	Порт (внутренний)	Описание
auth-service	8002	Регистрация, логин, пользователи
task-service	8000	Задачи, проекты, сотрудники
notification-service	8000	Уведомления
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

CI/CD (GitHub Actions)

Тесты
bash
cd auth-service
python manage.py test --settings=config.test_settings

cd ../task-service
python manage.py test --settings=config.test_settings

cd ../notification-service
python manage.py test --settings=config.test_settings
Покрытие тестами
auth-service: 96%

task-service: 97%

notification-service: 96%

CI/CD
Автоматический деплой в Yandex Cloud при пуше в feature/ci-cd.

Структура проекта
text
employee-task-tracker/
├── auth-service/
├── task-service/
├── notification-service/
├── frontend/
├── docker-compose.yml
└── README.md