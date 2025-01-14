lint:
	poetry run flake8 task_manager

install:
	poetry install

dev:
	poetry run python3 manage.py runserver

migrate:
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate

build:
	./build.sh

start:
	poetry run gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

test:
	poetry run python3 manage.py test

testcov:
	poetry run coverage run --source='.' manage.py test

makemessages:
	poetry run django-admin makemessages --ignore="static" --ignore=".env"  -l ru

compilemessages:
	poetry run django-admin compilemessages
