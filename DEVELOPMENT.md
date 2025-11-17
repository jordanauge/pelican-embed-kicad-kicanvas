# Development with uv

This project uses [uv](https://docs.astral.sh/uv/) for fast Python package management.

## Why uv?

- **10-100x faster** than pip
- **Consistent** lock file for reproducible installs
- **Simple** - single tool for package management
- **Rust-powered** - blazing fast dependency resolution

## Installation

### Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### Install project dependencies

```bash
# Basic installation (for using the plugin)
uv pip install -e .

# With optional liquid tag support
uv pip install -e ".[liquid]"

# With development dependencies (testing, linting)
uv pip install -e ".[liquid,dev]"
```

## Common Tasks

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ -v --cov=pelican_kicad_embed --cov-report=term --cov-report=html
```

### Linting & Formatting

```bash
# Check code style
uv run ruff check pelican_kicad_embed tests

# Auto-fix issues
uv run ruff check --fix pelican_kicad_embed tests

# Format code
uv run ruff format pelican_kicad_embed tests
```

### Type Checking

```bash
uv run pyright pelican_kicad_embed
```

### Building

```bash
# Build wheel and sdist
uv build

# Output: dist/pelican_embed_kicad_kicanvas-*.whl
#         dist/pelican-embed-kicad-kicanvas-*.tar.gz
```

## Using Justfile (Optional)

If you have [just](https://github.com/casey/just) installed:

```bash
# Show all available commands
just

# Install dependencies
just install-all

# Run tests
just test

# Run all checks (lint + typecheck + test)
just check

# Build package
just build
```

## CI/CD

GitHub Actions workflows automatically use `uv` for:

- Fast dependency installation
- Consistent testing across Python versions
- Quick builds for releases

## Comparison: pip vs uv

```bash
# Old way (pip)
pip install -e .[liquid,dev]        # ~10-30 seconds

# New way (uv)
uv pip install -e ".[liquid,dev]"   # ~1-3 seconds ⚡
```

## Migration Notes

- `uv` is a drop-in replacement for `pip`
- All `pip` commands work with `uv pip`
- No lock file needed for this library (used by end users)
- For applications, use `uv lock` to create `uv.lock`
