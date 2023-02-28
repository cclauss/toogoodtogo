FROM python:3.11.1-alpine

ENV DJANGO_SETTINGS_MODULE=toogoodtogo.settings.production \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.3.2

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --with production --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code

# Collect static files
RUN poetry run python manage.py collectstatic --noinput

RUN addgroup -S toogoodtogo && adduser -D -S -H -G toogoodtogo toogoodtogo
USER toogoodtogo

CMD ["gunicorn", "toogoodtogo.wsgi:application", "--bind", "0.0.0.0:8000"]
