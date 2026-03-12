import os

from polyglossia.settings.base import *

DEBUG = False

CSRF_TRUSTED_ORIGINS = [
    "https://polyglossia.tojest.dev",
]

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "polyglossia.tojest.dev",
]


ROLLBAR_ACCESS_TOKEN = os.environ['ROLLBAR_ACCESS_TOKEN']
ROLLBAR_ENVIRONMENT = os.environ['ROLLBAR_ENVIRONMENT']

# settings.py

ROLLBAR = {
    'access_token': os.getenv('ROLLBAR_ACCESS_TOKEN'),
    'environment': 'development' if DEBUG else 'production',
    'code_version': os.getenv('GIT_SHA', '1.0.0'),
    'root': BASE_DIR,
}
