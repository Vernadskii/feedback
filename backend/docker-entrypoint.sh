#!/bin/bash
set -e

if [ "$1" = "run" ]; then
  exec poetry run /app/src/manage.py runserver 0.0.0.0:8000
elif [ "$1" = "migrate" ]; then
  exec poetry run /app/src/manage.py migrate
elif [ "$1" = "linters" ]; then
  exec poetry run flake8
else
  exec "$@"
fi