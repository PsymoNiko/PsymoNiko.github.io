#!/bin/sh

python manage.py makemigrations 
python manage.py migrate --no-input
python manage.py collectstatic --no-input

python manage.py runserver 0.0.0.0:8000 
gunicorn core.wsgi:application --workers 3 --bind 0.0.0.0:8000
