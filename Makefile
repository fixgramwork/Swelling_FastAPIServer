.PHONY: install dev test lint docker-up docker-down

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -e ".[dev]"

dev:
	. .venv/bin/activate && python scripts/run_local.py

test:
	. .venv/bin/activate && pytest

lint:
	. .venv/bin/activate && ruff check .

docker-up:
	docker compose up --build

docker-down:
	docker compose down
