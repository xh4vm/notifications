#!/bin/sh

HOSTNAME=`env hostname`
echo -e "\033[32mStarting notice-admin_panel service: " $HOSTNAME "\033[0m"

if [ "$DJANGO_SERVICE" ]; then
  echo -e "\033[32mDJANGO_SERVICE: " $DJANGO_SERVICE "\033[0m"
  python manage.py collectstatic --no-input
  python manage.py migrate
fi

exec "$@"

#python manage.py collectstatic --no-input
#python manage.py migrate
#gunicorn config.wsgi:application --bind 0.0.0.0:$ADMIN_PANEL_PORT