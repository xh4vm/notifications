#!/bin/bash 

python manage.py flush --no-input
python manage.py collectstatic --no-input
python manage.py migrate
gunicorn config.wsgi:application --bind 0.0.0.0:$ADMIN_PANEL_PORT