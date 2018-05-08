GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")

APP_NAME:="davis-interactive"
VERSION:=0.0.1

.PHONY: build
build:
	docker build -t gcr.io/$(GCLOUD_PROJECT)/$(APP_NAME):$(VERSION) .

.PHONY: push
push: build
	gcloud docker -- push gcr.io/$(GCLOUD_PROJECT)/$(APP_NAME):$(VERSION)
