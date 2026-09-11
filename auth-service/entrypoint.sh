#!/bin/bash
set -e

echo "Applying migrations..."
python manage.py migrate

echo "Creating demo user..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='demo').exists():
    User.objects.create_user(username='demo', email='demo@example.com', password='demo12345')
    print('Demo user created')
else:
    print('Demo user already exists')
"

echo "Starting server..."
exec "$@"