GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")

APP_NAME:="davis-interactive"
VERSION:=0.0.1

.PHONY: build push run bash

build:
	docker build -t gcr.io/$(GCLOUD_PROJECT)/$(APP_NAME):$(VERSION) .

push: build
	gcloud docker -- push gcr.io/$(GCLOUD_PROJECT)/$(APP_NAME):$(VERSION)

run: build
	# This is for local development with a SQLite DB
	docker run -it \
		-e GUNICORN=1 \
		-v $(shell pwd)/data/DAVIS:/data/DAVIS \
		-v $(shell pwd)/db.sqlite3:/app/db.sqlite3 \
		-p 8000:8000 \
		gcr.io/$(GCLOUD_PROJECT)/$(APP_NAME):$(VERSION)

bash: build
	docker run -it \
		gcr.io/$(GCLOUD_PROJECT)/$(APP_NAME):$(VERSION) /bin/bash
