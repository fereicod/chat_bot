.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make Shows a list of all available commands.\033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Dependencies
.PHONY: install
install:  ## Installs dependencies
	@command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh
	uv sync --dev
	uv lock

##@ Testing
.PHONY: test
test:  ## Runs the automated test suite.
	uv run pytest

##@ Service Management
.PHONY: run
run:  ## Starts all services (API and database) in detached mode.
	docker compose up -d

.PHONY: down
down:  ## Stops and removes the containers of the running services.
	docker compose down

.PHONY: clean
clean: down  ## Stops the services, and removes associated containers and volumes.
	docker system prune -f
