from .base import *

DEBUG = True

SECRET_KEY = 'an absolutely not secrey key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'too_good_to_go',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost'

    }
}

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}