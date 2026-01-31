## Makefile for common development tasks

PYTHON ?= python

install:
	@echo "Installing project and development dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .[dev]

lint:
	@echo "Running ruff..."
	ruff src

typecheck:
	@echo "Running mypy..."
	mypy src

test:
	@echo "Running pytest..."
	pytest -q

format:
	@echo "Formatting code with ruff..."
	ruff format src

pre-commit-install:
	pre-commit install

run-api:
	@echo "Starting Flask API..."
	export FLASK_APP=src/portfolio_analytics/presentation/api/app.py && \
	$(PYTHON) -m flask run --host $${API_HOST:-0.0.0.0} --port $${API_PORT:-8000}

.PHONY: install lint typecheck test format pre-commit-install run-api