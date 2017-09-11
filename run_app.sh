#!/bin/sh
#python manage.py runserver -D
./venv2/bin/gunicorn -b0.0.0.0:19001 app:app

