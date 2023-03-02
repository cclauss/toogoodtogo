FROM python:3.11.1-alpine

# Set environment variables:
  # production mode
ENV DJANGO_SETTINGS_MODULE=toogoodtogo.settings.production \
  # don't buffer stdout and stderr (docker already does this, doing it again will cause double line breaks)
  PYTHONUNBUFFERED=1 \
  # don't create a pip cache (docker build won't use it anyway)
  PIP_NO_CACHE_DIR=off \
  # don't check for pip updates (we want deterministic and repeatable builds, we use the embeeded pip version)
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  # meeeeh, specified in env var mostly for convenience/clarity. Could also be inlined.
  POETRY_VERSION=1.3.2

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Tell where we will work from now on:
WORKDIR /code

# Copy only requirements, to avoid full rebuild on every slightest code change:
COPY poetry.lock pyproject.toml /code/

# Tell Poetry to not create a virtualenv in the container (it's already contained), and install dependencies:
RUN poetry config virtualenvs.create false \
  && poetry install --with production --no-interaction --no-ansi

# Copy the actual code:
COPY . /code

# Collect static files
RUN poetry run python manage.py collectstatic --noinput

# Create a sytem user and run as non-root (your security officer will thank you when you get p0wned):
RUN addgroup -S toogoodtogo && adduser -D -S -H -G toogoodtogo toogoodtogo
USER toogoodtogo

# Run the application. We need to bind to 0.0.0.0, 127.0.0.1 will not work when in Docker:
CMD ["gunicorn", "toogoodtogo.wsgi:application", "--bind", "0.0.0.0:8000"]
