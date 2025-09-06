#!/usr/bin/env sh
set -e
cd /grupi
python manage.py collectstatic --noinput
python manage.py migrate --noinput
exec "$@"
