# these will speed up builds, for docker compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: down build up test

build:
	docker compose build

buildprod:
	docker compose -f ./docker-compose.prod.yml build app

rebuild:
	docker compose build --no-cache

rebuildprod:
	docker compose -f ./docker-compose.prod.yml build --no-cache app

up:
	docker compose up -d app

upn:
	docker compose up app


upp:
	docker compose -f ./docker-compose.prod.yml up app

down:
	docker compose down --remove-orphans

startapp:
	docker compose run --rm app sh -c "python manage.py startapp $(app)" 

migrations:
	docker compose run --rm app sh -c "python manage.py makemigrations && python manage.py migrate" 

superuser:
	docker compose run --rm app sh -c "python manage.py createsuperuser" 

test: up
	# docker compose run --rm --no-deps --entrypoint=pytest app /tests/unit /tests/integration /tests/e2e
	docker compose run --rm --no-deps app sh -c 'pytest */tests/unit */tests/integration */tests/e2e'

lint: up
	# docker compose run --rm --no-deps --entrypoint=pytest app /tests/unit /tests/integration /tests/e2e
	docker compose run --rm --no-deps app sh -c 'flake8'

# unit-tests: up
# 	# docker compose run --rm --no-deps --entrypoint=pytest app */tests/unit
# 	docker compose run --rm --no-deps app sh -c 'pytest */tests/unit'

unit-tests: up
	docker compose run --rm --no-deps app sh -c "python manage.py test" 

integration-tests: up
	docker compose run --rm --no-deps --entrypoint=pytest app /tests/integration

e2e-tests: up
	docker compose run --rm --no-deps app sh -c 'pytest */tests/e2e'

logs:
	docker compose logs app | tail -100

# black:
# 	black -l 86 $$(find * -name '*.py')
