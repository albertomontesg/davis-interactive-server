build:
	docker-compose -f docker-compose.yml build

run:
	docker-compose -f docker-compose.yml up

stop:
	docker-compose -f docker-compose.yml down
