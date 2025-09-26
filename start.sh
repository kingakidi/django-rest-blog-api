#!/bin/bash

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Start gunicorn
exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 --keep-alive 2 --max-requests 1000 --max-requests-jitter 100 blog.wsgi:application
