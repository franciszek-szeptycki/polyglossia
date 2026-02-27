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
