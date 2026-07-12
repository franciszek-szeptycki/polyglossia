import os

from polyglossia.settings.base import *

import rollbar

DEBUG = False

LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "app.log"),
            "maxBytes": 10 * 1024 * 1024,  # 10 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["file"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

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
    'access_token': ROLLBAR_ACCESS_TOKEN,
    'environment': ROLLBAR_ENVIRONMENT,
    'code_version': os.getenv('GIT_SHA', '1.0.0'),
    'root': BASE_DIR,
}

rollbar.init(**ROLLBAR)
