#!/bin/bash

function manage_app() {
	python3 manage.py makemigrations
	python3 manage.py migrate
}

function start_development() {
	# use django runserver as development server here.
	manage_app
	python3 manage.py runserver 0.0.0.0:8000
}

function start_production() {
	# use gunicorn for production server here
	manage_app
	export DJANGO_SETTINGS_MODULE=server.settings.production
	gunicorn server.wsgi -w 4 -b 0.0.0.0:8000 --chdir=/app --log-file -
}

if [ ${PRODUCTION} == "true" ]; then
	# use production server
	start_production
else
	# use development server
	start_development
fi
