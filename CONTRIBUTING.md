# Contributing to pelican-embed-kicad-kicanvas

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pelican-embed-kicad-kicanvas.git
   cd pelican-embed-kicad-kicanvas
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode:
   ```bash
   pip install -e .
   pip install -e .[liquid]  # For Liquid Tag support
   ```

## Running Tests

```bash
# Run tests (when test suite is added)
python -m pytest tests/
```

## Code Style

- Follow PEP 8 guidelines
- Use docstrings for all functions and classes
- Add type hints where applicable
- Keep line length under 100 characters

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit with clear messages (`git commit -m 'Add amazing feature'`)
5. Push to your fork (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Reporting Bugs

Please open an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (Python version, Pelican version, OS)

## Feature Requests

Open an issue describing:
- The feature you'd like
- Why it would be useful
- Possible implementation approach (optional)

Thank you for your contributions! 🎉
