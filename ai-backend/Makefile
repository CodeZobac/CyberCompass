.PHONY: help install dev test test-unit test-integration test-performance lint format clean docker-build docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install           - Install dependencies with uv"
	@echo "  make dev              - Run development server"
	@echo "  make test             - Run all tests"
	@echo "  make test-unit        - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make test-performance - Run performance tests"
	@echo "  make lint             - Run linters"
	@echo "  make format           - Format code"
	@echo "  make clean            - Clean temporary files"
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-up        - Start Docker containers"
	@echo "  make docker-down      - Stop Docker containers"

install:
	@command -v uv >/dev/null 2>&1 || { echo "Installing uv..."; curl -LsSf https://astral.sh/uv/install.sh | sh; }
	uv sync

dev:
	uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

test:
	uv run pytest

test-unit:
	uv run pytest tests/unit -v

test-integration:
	@echo "Running CrewAI Integration Tests..."
	uv run python tests/integration/test_runner.py

test-performance:
	@echo "Running Performance Tests..."
	uv run python tests/integration/test_runner.py --performance

lint:
	uv run ruff check src tests
	uv run mypy src

format:
	uv run black src tests
	uv run ruff check --fix src tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache .ruff_cache .venv

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down
