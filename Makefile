GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")

APP_NAME:="davis-interactive"
VERSION:=0.0.1

.PHONY: build
build:
	docker build -t gcr.io/$(GCLOUD_PROJECT)/$(APP_NAME):$(VERSION) .

.PHONY: push
push: build
	gcloud docker -- push gcr.io/$(GCLOUD_PROJECT)/$(APP_NAME):$(VERSION)

.PHONY: run
run: build
	# This is for local development with a SQLite DB
	docker run -it \
		-e GUNICORN=1 \
		-v $(shell pwd)/data/DAVIS:/data/DAVIS \
		-v $(shell pwd)/db.sqlite3:/app/db.sqlite3 \
		-p 8000:8000 \
		gcr.io/$(GCLOUD_PROJECT)/$(APP_NAME):$(VERSION)
