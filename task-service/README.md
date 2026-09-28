# task-service

Сервис управления задачами, сотрудниками и проектами.

## Стек

- Django 4 + DRF
- PostgreSQL (`task_db`)
- JWT (stateless, валидация без БД юзеров)

## Запуск локально

См. корневой [README](../README.md).

## Эндпоинты

| Метод | URL | Описание |
|---|---|---|
| CRUD | `/api/employees/` | Сотрудники |
| GET | `/api/employees/busy/` | Занятые сотрудники с их задачами |
| CRUD | `/api/tasks/` | Задачи |
| GET | `/api/tasks/important/` | Важные задачи + кандидаты |
| CRUD | `/api/projects/` | Проекты |

## Swagger

http://localhost:8003/api/docs/

## Переменные окружения

- `SECRET_KEY` — Django SECRET_KEY
- `POSTGRES_DB` — `task_db`
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`

## Тесты

```bash
python manage.py test --settings=config.test_settings
```

Покрытие: 97% (90 тестов).

## Линтер

```bash
flake8 .
```