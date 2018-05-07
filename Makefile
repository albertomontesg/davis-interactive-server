# build:
# 	docker-compose -f docker-compose.yml build

# run:
# 	docker-compose -f docker-compose.yml up

# stop:
# 	docker-compose -f docker-compose.yml down

# .PHONY: all
# all: deploy

GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")
APP_NAME:="davis-interactive"

.PHONY: build
build:
	docker build -t gcr.io/$(GCLOUD_PROJECT)/$(APP_NAME) .

.PHONY: push
push: build
	gcloud docker -- push gcr.io/$(GCLOUD_PROJECT)/$(APP_NAME)
