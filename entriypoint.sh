#!/bin/bash

# Activate virtualenv
source /opt/env/bin/activate

# Wait for DB (optional)
# ./wait-for-it.sh db:5432 -- echo "Database is up"

# Run based on DEBUG value
if [ "$DEBUG" = "true" ]; then
    echo "Running in development mode"
    python manage.py runserver 0.0.0.0:8000
else
    echo "Running in production mode with Gunicorn"
    gunicorn _core.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 4 \
        --timeout 120 \
        --log-level info
fi
