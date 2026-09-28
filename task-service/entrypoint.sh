#!/bin/bash
set -e

echo "Applying migrations..."
python manage.py migrate

echo "Starting server..."
exec "$@"