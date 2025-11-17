.PHONY: help install test lint typecheck verify update-kicanvas clean

help:
	@echo "Available targets:"
	@echo "  install          Install package in development mode"
	@echo "  test             Run pytest tests"
	@echo "  lint             Run code linting (ruff)"
	@echo "  typecheck        Run type checking (pyright)"
	@echo "  verify           Run all verification checks (lint + typecheck + dependency check)"
	@echo "  update-kicanvas  Update KiCanvas to latest version"
	@echo "  clean            Remove build artifacts"

install:
	pip install -e .

test:
	pytest tests/ -v

lint:
	@./scripts/lint.sh

typecheck:
	@./scripts/typecheck.sh

verify: lint typecheck
	@echo "🔍 Checking KiCanvas version..."
	@python3 scripts/check_kicanvas_version.py

update-kicanvas:
	@./scripts/update_kicanvas.sh

clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
