#!/bin/bash
python manage.py migrate

gunicorn core.wsgi --bind 0.0.0.0:8000 -w 4 --access-logfile '-' --error-logfile '-' --timeout 600