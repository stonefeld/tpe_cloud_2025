#!/usr/bin/env sh
set -e

cd /app/tpe_cloud

uv run python manage.py migrate --noinput

exec "$@"
