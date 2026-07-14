.PHONY: install test lint typecheck coverage clean run

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --tb=short

lint:
	ruff check agentos/ tests/
	ruff format --check agentos/ tests/

typecheck:
	mypy agentos/

coverage:
	pytest tests/ --cov=agentos --cov-report=html --cov-report=term-missing

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf dist/ build/ *.egg-info .coverage htmlcov/

run:
	agentos run --goal "$(GOAL)"



