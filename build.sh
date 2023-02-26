#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install --with production

python manage.py collectstatic --no-input
python manage.py migrate
