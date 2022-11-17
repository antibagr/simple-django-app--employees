SHELL:=bash

.PHONY: setup
install:
	@poetry install --no-root

.PHONY: safety
safety:
	poetry run safety check --full-report -i 42194
	poetry run pip check
	poetry check

.PHONY: lint
lint:
	poetry run mypy . --disable-error-code str-format
	poetry run flake8

.PHONY: format
format:
	@poetry run black ./src ./tests
	@poetry run isort ./src ./tests

.PHONY: format-check
format-check:
	poetry run black ./src --check
	poetry run isort ./src --check-only

.PHONY: test
test:
	@poetry run pytest -vv

.PHONY: test-cov
test-cov:
	poetry run pytest \
		--cov=app --cov=db --cov=external \
		--cov-report=xml --cov-report=html --cov-report=term-missing:skip-covered \
		--cov-fail-under=0.0

.PHONY: migrations
migrations:
	@poetry run python app/manage.py makemigrations

.PHONY: migrate
migrate:
	@poetry run python app/manage.py migrate

.PHONY: compose-up
compose-up:
	@docker-compose -f contrib/docker-compose.yml up -d --build

.PHONY: compose-down
compose-down:
	-@docker-compose -f contrib/docker-compose.yml down --remove-orphans

.PHONY: compose-migrations
compose-migrations:
	@docker-compose -f contrib/docker-compose.yml -f contrib/docker-compose.local-web-migrations.yml up -d --build
	-@docker-compose -f contrib/docker-compose.yml -f contrib/docker-compose.local-web-migrations.yml down

.PHONY: run-web
run-web:
	@poetry run uvicorn --factory src.asgi:get_app --host 0.0.0.0 --port 8000

.PHONY: db-seed
db-seed:
	@docker-compose -f contrib/docker-compose.yml exec postgres psql employees -d employees -f /seed/seed.sql