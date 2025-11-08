.PHONY: help install dev-install test lint format clean

help:
	@echo "Available commands:"
	@echo "  make install      - Install package"
	@echo "  make dev-install  - Install package with dev dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters (ruff, mypy)"
	@echo "  make format       - Format code with black"
	@echo "  make clean        - Remove build artifacts"

install:
	poetry install

dev-install:
	poetry install --with dev

test:
	poetry run pytest -v

lint:
	poetry run ruff check src tests
	poetry run mypy src

format:
	poetry run black src tests
	poetry run ruff check --fix src tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
