#!/bin/bash


python manage.py collectstatic --noinput
python manage.py migrate
#python manage.py collectstatic --noinput
gunicorn -b 0.0.0.0:8000 -w 3 core.wsgi:application

