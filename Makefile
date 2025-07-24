.PHONY: up down airflow-init airflow-up lint format test

up:
	docker compose -f docker/docker-compose.yml up -d --build

down:
	docker compose -f docker/docker-compose.yml down -v

airflow-init:
	docker compose -f docker/docker-compose.yml run --rm airflow-init

airflow-up:
	docker compose -f docker/docker-compose.yml up -d airflow-webserver airflow-scheduler

lint:
	ruff check src tests

format:
	ruff check src tests --fix

test:
	pytest -q
