#!/usr/bin/env bash
# exit on error
set -o errexit

pip install poetry==1.3.2
poetry install --with production

python manage.py collectstatic --no-input
python manage.py migrate
