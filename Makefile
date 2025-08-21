.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage\n make <target>\033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Dependencies
.PHONY: install
install:  ## Install all requirements to run the service.
	@echo "🔍 Checking required tools..."

	# Check curl
	@if ! command -v curl >/dev/null 2>&1; then \
		echo "❌ 'curl' is not installed."; \
		echo "   👉 Install it with: sudo apt install curl    # Debian/Ubuntu"; \
		echo "   👉 Or: brew install curl                     # macOS"; \
		exit 1; \
	fi

	# Check Python
	@if ! command -v python3 >/dev/null 2>&1; then \
		echo "❌ 'python3' is not installed."; \
		echo "   👉 Install it with: sudo apt install python3 # Debian/Ubuntu"; \
		echo "   👉 Or: brew install python                   # macOS"; \
		exit 1; \
	fi

	# Check Docker
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "❌ 'docker' is not installed."; \
		echo "   👉 Follow instructions at: https://docs.docker.com/get-docker/"; \
		exit 1; \
	fi

	# Check Docker Compose
	@if ! docker compose version >/dev/null 2>&1; then \
		echo "❌ 'docker compose' is not available."; \
		echo "   👉 Follow instructions at: https://docs.docker.com/compose/install/"; \
		exit 1; \
	fi

	# Check UV
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "⬇️  Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi

	@echo "📦 Syncing dependencies with uv..."
	uv sync --dev
	uv lock

	@echo "✅ Installation complete. Virtual environment ready."

##@ Testing
.PHONY: test
test:  ## Runs the automated test suite.
	@echo "🔍 Running tests..."
	uv run pytest

##@ Service Management
.PHONY: run
run:  ## Starts all services (API and database) in detached mode.
	docker compose up -d
	@echo "✅ Services started successfully."

.PHONY: run-build
run-build:  ## Build and run with logs visible
	@echo "🚀 Building and starting all services with logs..."
	docker compose up --build

.PHONY: run-reset-db
run-reset-db:  ## Build all services and reset the database
	docker compose up --build -d
	@echo "⏳ Waiting a few seconds for MySQL to start..."
	@sleep 5
	docker compose exec -T mysql /docker-entrypoint-initdb.d/run-reset.sh
	@echo "✅ Services started and database reset successfully."

.PHONY: up-logs
up-logs:  ## Show logs of all running services
	@echo "📋 Showing logs of all running services..."
	docker compose logs -f

.PHONY: down
down:  ## Stops and removes the containers of the running services.
	@echo "🔴 Stopping services..."
	docker compose down

.PHONY: clean
clean: down  ## Stops the services and removes associated containers and volumes
	@echo "⚠️  This will remove all containers AND volumes for this project!"
	@read -p "Are you sure? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		docker compose down -v; \
		echo "✅ Containers and volumes removed."; \
	else \
		echo "❌ Aborted."; \
	fi
