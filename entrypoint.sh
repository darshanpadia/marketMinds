#!/usr/bin/env bash
set -e

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

echo "Creating admin user..."
python create_admin.py

if [ "$1" = "runserver" ]; then
  echo "Starting Django server..."
  exec python manage.py runserver 0.0.0.0:8000
elif [ "$1" = "celery" ]; then
  echo "Starting Celery worker..."
  exec celery -A marketMinds worker --loglevel=info --concurrency=2
else
  echo "Running custom command: $@"
  exec "$@"
fi
