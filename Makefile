.PHONY: help supabase
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
supabase:
	npx supabase start -x edge-runtime,inbucket
supabase-stop:
	npx supabase stop
dev: ## Run server
	uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
css: ## Build css with tailwind
	# tailwindcss -i styles/main.css -o static/css/main.css
	npx tailwindcss -i ./frontend/global.css -o ./static/styles/main.css
css-watch: ## Build css with tailwind
	# tailwindcss -i styles/main.css -o static/css/main.css --watch
	npx tailwindcss -i ./frontend/global.css -o ./static/styles/main.css --watch
test: ## Run tests using docker compose
	docker compose run --build --rm test ; \
	docker compose down --remove-orphans
run:
	uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --proxy-headers
