.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make <target>\033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: install
install:  ## Install all requirements
	@command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh
	uv sync --dev
	uv lock

##@ Testing
.PHONY: test
test:  ## Run tests
	uv run pytest

##@ Service Management
.PHONY: run
run:  ## Run the service and related services in Docker
	docker compose up -d

.PHONY: down
down:  ## Teardown all running services
	docker compose down

.PHONY: clean
clean: down  ## Teardown and remove all containers, networks, and volumes
	docker system prune -f
