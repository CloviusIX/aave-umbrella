.PHONY: all venv setup depfreeze lint

PYTHON ?= .venv/bin/python
PIP ?= .venv/bin/pip
DOCKER_COMPOSE ?= docker compose

all: setup

venv:
	# Check if the .venv directory exists, if not create it
	# Update the .venv directory to the latest version (pip, setuptools, etc)
	[ -d .venv ] || python3 -m venv --upgrade-deps .venv

setup: venv
	# Upgrade/install wheel to the latest version.
	# Wheel is a package format for Python that speeds up package installation by avoiding the need for
	# running setup.py and compilation, which makes it a preferred format over source archives.
	$(PIP) install --upgrade wheel

	# Install all dependencies listed in requirements.txt into the virtual environment
	$(PIP) install -r requirements.txt

depfreeze: venv
	# Generate a requirements.txt file with all the dependencies installed in the virtual environment
	$(PIP) freeze > requirements.txt

lint: venv
	$(PYTHON) -m ruff check --select I --fix
	$(PYTHON) -m ruff format
	$(PYTHON) -m mypy .
	$(PYTHON) -m ruff check --fix

docker-up:
	$(DOCKER_COMPOSE) up -d

docker-down:
	$(DOCKER_COMPOSE) down