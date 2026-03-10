#!/bin/bash

set -ex

source venv/bin/activate

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

gunicorn 'polyglossia.wsgi' --bind=0.0.0.0:8000 --workers=3
