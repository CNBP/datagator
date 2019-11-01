#!/usr/bin/env bash
source venv/bin/activate
flask db upgrade
#flask translate compile
exec gunicorn -b:5000 --acess-logfile  - --error-logfile - datagator:app