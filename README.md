# Task Manager
[![Actions Status](https://github.com/vitallcore/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/vitallcore/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/d1258a96be3ef5b67aee/maintainability)](https://codeclimate.com/github/vitallcore/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d1258a96be3ef5b67aee/test_coverage)](https://codeclimate.com/github/vitallcore/python-project-52/test_coverage)

## Description
Task Manager is a simple web application that helps users manage their tasks.

## Installation
Clone this repository to your local machine.
```bash
git clone https://github.com/vitallcore/python-project-52.git
cd python-project-52
```
Install dependencies using [Poetry](https://python-poetry.org/docs/).
```bash
make install
```
Create the new .env file and define SECRET_KEY, DEBUG, DATABASE_URL and WEB_CONCURRENCY variables there. For example,
```bash
echo "SECRET_KEY=secret_key" >> .env
echo "DEBUG=False" >> .env
echo "DATABASE_URL=postgresql://user:password@host:port/database_name" >> .env
echo "WEB_CONCURRENCY=4" >> .env
```
Initialize the build script.
```bash
make build
```
Run the app.
```bash
# using Gunicorn
make start

# or using the Django development server with debug mode
make dev
```

## Demo
Check out Task Manager by clicking [here](https://python-project-52-c8dp.onrender.com).
