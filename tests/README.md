# Testing Guide

This directory contains unit tests for the pelican-embed-kicad-kicanvas plugin.

## Running Tests

### Run all tests

```bash
python -m pytest tests/
```

Or using unittest:

```bash
python -m unittest discover tests/
```

### Run specific test file

```bash
python -m pytest tests/test_md_ext.py
python -m pytest tests/test_rst_directive.py
```

### Run specific test case

```bash
python -m pytest tests/test_md_ext.py::TestMarkdownExtension::test_basic_syntax
```

## Test Coverage

### Current test coverage includes:

- **Markdown Extension** (`test_md_ext.py`):
  - Basic syntax parsing
  - Style parameter handling
  - Controls parameter handling
  - All parameters combined
  - Filenames without quotes
  - Multiple embeddings on same line
  - Content preservation

- **reStructuredText Directive** (`test_rst_directive.py`):
  - Basic directive syntax
  - Style option handling
  - Controls option handling
  - All options combined
  - Multiple directives in document
  - Directive embedded in larger document

### Future test coverage needs:

- Signal handling (`inject_kicanvas_script`)
- Pelican integration tests
- Liquid Tag handler (requires liquid_tags)
- End-to-end browser tests with KiCanvas

## Dependencies

Tests require the following packages:

```bash
pip install pytest
pip install pelican
pip install markdown
pip install docutils
```

## CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7, 3.8, 3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -e .
        pip install pytest
    - name: Run tests
      run: pytest tests/
```
