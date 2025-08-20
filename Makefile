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
	uv run pytest

##@ Service Management
.PHONY: run
run:  ## Starts all services (API and database) in detached mode.
	docker compose up -d

.PHONY: run-build
run-build:  ## Build and run with logs visible
	docker compose up --build

.PHONY: down
down:  ## Stops and removes the containers of the running services.
	docker compose down

.PHONY: clean
clean: down  ## Stops the services, and removes associated containers and volumes.
	docker system prune -f
