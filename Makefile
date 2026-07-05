COMPOSE=docker compose -f infrastructure/docker/docker-compose.yml --env-file .env

up:
	$(COMPOSE) up --build -d

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

migrate:
	docker exec -it midc-backend alembic upgrade head

revision:
	docker exec -it midc-backend alembic revision --autogenerate -m "$(m)"

shell:
	docker exec -it midc-backend bash

db:
	docker exec -it midc-postgres psql -U midc_user -d midc_db

docker_run:
	docker compose -f infrastructure/docker/docker-compose.yml --env-file .env up --build

.PHONY: install run-backend test lint

install:
	pip install -r apps/backend/requirements.txt

run-backend:
	uvicorn apps.backend.app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest apps/backend/tests

lint:
	ruff check .
