.PHONY: help install run test clean docker-build docker-run docker-stop

help: ## Show this help message
	@echo "CARFAX VIN Checker - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dependencies
	pip install -r requirements.txt

run: ## Run the application in development mode
	python run.py

test: ## Run tests
	python -m pytest tests/ -v

clean: ## Clean up cache files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

docker-build: ## Build Docker image
	docker build -t carfax-app .

docker-run: ## Run with Docker Compose
	docker-compose up -d

docker-stop: ## Stop Docker containers
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

dev: ## Run in development mode with auto-reload
	FLASK_ENV=development FLASK_DEBUG=1 python run.py

prod: ## Run in production mode
	FLASK_ENV=production gunicorn -w 4 -b 0.0.0.0:8080 run:app

format: ## Format code with black
	black app/ scripts/ run.py

lint: ## Lint code with flake8
	flake8 app/ scripts/ run.py

check: format lint ## Format and lint code 