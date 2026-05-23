.DEFAULT_GOAL := help
PYTHONPATH    := .
PYTHON        := PYTHONPATH=$(PYTHONPATH) python3

.PHONY: help dev stop db lint test connector example clean

help:  ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

# ---------------------------------------------------------------------------
# Development environment
# ---------------------------------------------------------------------------

dev:  ## Start Postgres + worker (docker compose up)
	cp -n .env.example .env 2>/dev/null || true
	docker compose up -d
	@echo ""
	@echo "  Postgres is up at localhost:5432"
	@echo "  Run 'make db' to initialise the schema"
	@echo "  Run 'make connector NAME=example' to run a connector"

stop:  ## Stop all containers
	docker compose down

db:  ## Initialise (or re-initialise) the database schema
	$(PYTHON) scripts/setup_db.py

db-reset:  ## Drop and recreate all tables (destroys all data — dev only)
	$(PYTHON) scripts/setup_db.py --reset

# ---------------------------------------------------------------------------
# Connectors
# ---------------------------------------------------------------------------

connector:  ## Run a connector by name, e.g. make connector NAME=example
ifndef NAME
	@echo "Usage: make connector NAME=<connector_dir_name>"
	@echo "       make connector NAME=example"
	@exit 1
endif
	$(PYTHON) connectors/$(NAME)/connector.py

example:  ## Run the example connector (mock data, no setup needed)
	$(PYTHON) connectors/example_connector.py

# ---------------------------------------------------------------------------
# Code quality
# ---------------------------------------------------------------------------

lint:  ## Run ruff linter
	ruff check connectors/ schema/ scripts/

format:  ## Auto-format with ruff
	ruff format connectors/ schema/ scripts/

typecheck:  ## Run mypy type checker
	mypy connectors/ schema/ --ignore-missing-imports

test:  ## Run test suite
	pytest tests/ -v

test-cov:  ## Run tests with coverage report
	pytest tests/ -v --cov=. --cov-report=term-missing

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

clean:  ## Remove Python cache files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
