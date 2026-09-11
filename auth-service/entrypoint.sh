#!/bin/bash
set -e

echo "Applying migrations..."
python manage.py migrate

echo "Creating demo user..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
demo, created = User.objects.get_or_create(
    username='demo',
    defaults={'email': 'demo@example.com'},
)
demo.email = 'demo@example.com'
demo.is_active = True
demo.is_staff = True
demo.set_password('demo12345')
demo.save()
print('Demo user created' if created else 'Demo user password refreshed')
"

echo "Starting server..."
exec "$@"