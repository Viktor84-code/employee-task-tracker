# notification-service

Сервис отправки email-уведомлений через Celery.

## Стек

- Django 4 + DRF
- PostgreSQL (`notif_db`)
- Redis + Celery (worker)

## Запуск локально

См. корневой [README](../README.md).

## Эндпоинты

| Метод | URL | Описание |
|---|---|---|
| POST | `/api/notifications/send/` | Поставить уведомление в очередь |

## Swagger

http://localhost:8004/api/docs/

## Переменные окружения

- `SECRET_KEY` — Django SECRET_KEY
- `POSTGRES_DB` — `notif_db`
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`
- `REDIS_URL` — `redis://redis:6379/0`

## Celery worker

Worker запускается отдельным контейнером `notification-worker`:

```bash
celery -A config worker -l info
```

## Тесты

```bash
python manage.py test --settings=config.test_settings
```