install:
	uv sync

build:
	./build.sh

migrate:
	uv run python3 manage.py migrate

makemigrations:
	uv run python3 manage.py makemigrations

dev:
	uv run python3 manage.py runserver 8000

start:
	uv run python3 -m gunicorn core.asgi:application -k uvicorn.workers.UvicornWorker

lint:
	uv run flake8

test:
	uv run python3 manage.py test

test-coverage:
	uv run coverage run manage.py test
	uv run coverage report
	uv run coverage xml

selfcheck:
	uv check

check: lint test

.PHONY: install test lint selfcheck check build
