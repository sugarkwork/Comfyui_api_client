.PHONY: help install install-dev test lint format clean build publish

help:
	@echo "Available commands:"
	@echo "  install      Install package"
	@echo "  install-dev  Install development dependencies"
	@echo "  test         Run tests"
	@echo "  lint         Run linting"
	@echo "  format       Format code"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build package"
	@echo "  publish      Publish to PyPI"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=comfyuiclient --cov-report=term-missing

lint:
	flake8 comfyuiclient tests
	mypy comfyuiclient
	black --check comfyuiclient tests
	isort --check-only comfyuiclient tests

format:
	black comfyuiclient tests
	isort comfyuiclient tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	python -m twine upload dist/*