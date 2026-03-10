#!/bin/bash

set -ex

python manage.py collectstatic --noinput

python manage.py migrate

gunicorn 'polyglossia.wsgi' --bind=0.0.0.0:8000 --workers=3
