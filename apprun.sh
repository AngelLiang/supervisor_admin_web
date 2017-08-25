#!/bin/sh
source venv2/bin/activate
python manage.py runserver -D
#gunicorn -w 4 -b 0.0.0.0:19001 app:app

