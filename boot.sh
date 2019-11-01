#!/usr/bin/env bash
source venv/bin/activate
flask db upgrade
#flask translate compile
# index:app here points Gunicorn to run the "app" from index.py
exec gunicorn -b :5000 --access-logfile - --error-logfile - index:app