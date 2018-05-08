#!/bin/bash

function manage_app() {
	python3 manage.py makemigrations
	python3 manage.py migrate
}

function start_default() {
	# use django runserver as development server here.
	manage_app
	python3 manage.py runserver 0.0.0.0:8000
}

function start_gunicorn() {
	NUM_WORKERS="${NUM_WORKERS:-4}"
	PORT=${PORT:8000}
	# use gunicorn for production server here
	manage_app
	gunicorn server.wsgi -w "$NUM_WORKERS" -b 0.0.0.0:"$PORT" --chdir=/app --log-file -
}

if [ ! -z "$GUNICORN" ]; then
	# use production server
	start_gunicorn
else
	# use development server
	start_default
fi
