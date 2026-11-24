ENV ?= development

ifeq ($(filter $(ENV),development staging production),)
$(error ENV must be development, staging, or production)
endif

COMPOSE = docker compose -f docker-compose.yml -f docker-compose.$(ENV).yml --env-file env/$(ENV).env

.DEFAULT_GOAL := help
.PHONY: help dev staging prod up down build restart ps logs logs-api logs-worker logs-frontend shell-api shell-worker shell-frontend config clean

help:
	@echo "Usage: make <target> [ENV=development|staging|production]"
	@echo ""
	@echo "  make dev                 Start development (hot reload, published ports)"
	@echo "  make staging             Start staging behind nginx on port 8080"
	@echo "  make prod                Start production behind nginx on port 80"
	@echo "  make up                  Start the selected ENV"
	@echo "  make down                Stop the selected ENV"
	@echo "  make build               Build images for the selected ENV"
	@echo "  make restart             Restart containers for the selected ENV"
	@echo "  make ps                  Show container status"
	@echo "  make logs                Follow logs for every service"
	@echo "  make logs-api            Follow API logs"
	@echo "  make logs-worker         Follow worker logs"
	@echo "  make logs-frontend       Follow frontend logs"
	@echo "  make shell-api           Shell into the API container"
	@echo "  make shell-worker        Shell into the worker container"
	@echo "  make shell-frontend      Shell into the frontend container"
	@echo "  make config              Print the merged Compose file"
	@echo "  make clean               Stop containers and delete volumes for the selected ENV"

dev:
	@$(MAKE) up ENV=development

staging:
	@$(MAKE) up ENV=staging

prod:
	@$(MAKE) up ENV=production

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

restart:
	$(COMPOSE) restart

ps:
	$(COMPOSE) ps

logs:
	$(COMPOSE) logs -f

logs-api:
	$(COMPOSE) logs -f api

logs-worker:
	$(COMPOSE) logs -f worker

logs-frontend:
	$(COMPOSE) logs -f frontend

shell-api:
	$(COMPOSE) exec api bash

shell-worker:
	$(COMPOSE) exec worker bash

shell-frontend:
	$(COMPOSE) exec frontend sh

config:
	$(COMPOSE) config

clean:
	$(COMPOSE) down -v --remove-orphans
