#!/bin/bash
set -e

if [ "$1" = "run" ]; then
  exec poetry run /app/src/manage.py runserver 0.0.0.0:8000
elif [ "$1" = "migrate" ]; then
  exec poetry run /app/src/manage.py migrate
else
  exec "$@"
fi