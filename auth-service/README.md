# auth-service

Сервис аутентификации и управления пользователями.

## Стек

- Django 4 + DRF
- PostgreSQL (`auth_db`)
- JWT (SimpleJWT)

## Запуск локально

См. корневой [README](../README.md).

## Эндпоинты

| Метод | URL | Описание |
|---|---|---|
| POST | `/api/auth/register/` | Регистрация пользователя |
| POST | `/api/auth/login/` | Получить access + refresh токены |
| POST | `/api/auth/refresh/` | Обновить access-токен |
| GET | `/api/auth/users/` | Список пользователей |

## Swagger

http://localhost:8002/api/docs/

## Переменные окружения

- `SECRET_KEY` — Django SECRET_KEY
- `POSTGRES_DB` — `auth_db`
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`
- `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`

## Тесты

```bash
python manage.py test --settings=config.test_settings
```