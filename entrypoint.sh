#!/bin/bash

echo "Ожидание запуска PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.5
done
echo "PostgreSQL готов!"

echo "Выполнение миграций..."
python manage.py migrate

python manage.py collectstatic --noinput

echo "Запуск Django сервера..."
exec python manage.py runserver 0.0.0.0:8000

