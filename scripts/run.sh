#!/usr/bin/env bash

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate  # Does nothing if there are no new migrations to apply.

uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi