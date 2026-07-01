.PHONY: install dev test lint docker-up docker-down k8s-build k8s-apply k8s-delete k8s-status k8s-port-forward

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

k8s-build:
	docker build -t swelling-fastapi-server:local .

k8s-apply:
	kubectl apply -k k8s/overlays/local

k8s-delete:
	kubectl delete -k k8s/overlays/local

k8s-status:
	kubectl get all -n swelling

k8s-port-forward:
	kubectl port-forward -n swelling svc/gateway 8000:8000
