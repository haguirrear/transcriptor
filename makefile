.PHONY: help
.ONESHELL:
SHELL = /bin/bash

help: ## Print help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_.-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
.DEFAULT_GOAL := help
clean:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete
	find . -name '__pycache__' -delete

dev: ## Run server
	uvicorn reveal.main:app --host 0.0.0.0 --port 8000 --reload
build-css: ## Build css with tailwind
	tailwindcss -i styles/main.css -o static/css/main.css --watch
test: ## Run tests using docker compose
	docker compose run --build --rm test ; \
	docker compose down --remove-orphans 

