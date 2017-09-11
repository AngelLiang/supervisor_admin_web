#!/bin/sh
./venv2/bin/gunicorn -b0.0.0.0:19001 manage:app

