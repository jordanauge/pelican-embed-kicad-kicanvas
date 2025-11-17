# Justfile for pelican-embed-kicad-kicanvas
# Requires: just (https://github.com/casey/just)
# Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh

# Default recipe - show help
default:
    @just --list

# Install dependencies using uv
install:
    uv pip install -e .

# Install with all optional dependencies
install-all:
    uv pip install -e ".[liquid,dev]"

# Run all tests
test:
    uv run pytest tests/ -v

# Run tests with coverage
test-cov:
    uv run pytest tests/ -v --cov=pelican_kicad_embed --cov-report=term --cov-report=html

# Run linting checks
lint:
    uv run ruff check pelican_kicad_embed tests

# Format code
format:
    uv run ruff format pelican_kicad_embed tests

# Type checking
typecheck:
    uv run pyright pelican_kicad_embed

# Clean build artifacts
clean:
    rm -rf build/ dist/ *.egg-info .pytest_cache .coverage htmlcov
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

# Build distribution packages
build: clean
    uv build

# Run all quality checks
check: lint typecheck test

# Sync dependencies with uv
sync:
    uv pip sync

# Create a new release (dry-run)
release-check version:
    @echo "Preparing release {{version}}"
    @echo "1. Update version in pelican_kicad_embed/__about__.py to {{version}}"
    @echo "2. Update CHANGELOG in README.md"
    @echo "3. Run: just test"
    @echo "4. Run: git commit -am 'Release {{version}}'"
    @echo "5. Run: git tag v{{version}}"
    @echo "6. Run: git push origin main --tags"
