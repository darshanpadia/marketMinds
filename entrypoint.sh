#!/usr/bin/env bash

echo "static"
python manage.py collectstatic --noinput
echo "migrate"
python manage.py migrate
echo "admin"
python create_admin.py
echo "runserver"
python manage.py runserver 0.0.0.0:8000
