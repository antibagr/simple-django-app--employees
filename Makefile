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
	@poetry run black ./app ./tests
	@poetry run isort ./app ./tests

.PHONY: format-check
format-check:
	poetry run black ./app --check
	poetry run isort ./app --check-only

.PHONY: migrations
migrations:
	@poetry run python app/manage.py makemigrations

.PHONY: migrate
migrate:
	@poetry run python app/manage.py migrate

.PHONY: runserver
migrate:
	@poetry run python app/manage.py runserver

.PHONY: db-seed
db-seed:
	@poetry run python dev/generate_initial.data.py
	@poetry run python app/manage.py loaddata data.json
	@rm -rf data.json