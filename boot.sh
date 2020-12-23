#!/bin/sh
source venv/bin/activate
exec gunicorn -b :8500 --access-logfile - --error-logfile - app --timeout 300
