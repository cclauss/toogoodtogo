import os

import dj_database_url

from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')

SECRET_KEY = os.environ['SECRET_KEY']

DATABASES = {
    'default': dj_database_url.config()
}

STATIC_ROOT = BASE_DIR / 'static'

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# should be in environment variables, or even not here at all (use something like Sentry)
ADMINS = [
    ('Mathieu Dupuy', 'deronnax@gmail.com')
]
