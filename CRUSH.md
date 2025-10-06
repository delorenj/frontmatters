# Frontmatters Development Guide

## Build/Lint/Test Commands

```bash
# Install dependencies
uv sync --dev

# Run all tests
uv run python -m pytest

# Run single test file
uv run python -m pytest tests/test_add_description.py

# Run with coverage
uv run python -m pytest --cov=frontmatters

# Linting and formatting
uv run ruff check .
uv run ruff format .
uv run black .
uv run mypy frontmatters/
```

## Code Style Guidelines

### Python Version & Formatting
- Python 3.12+ required
- Line length: 88 characters (Black/Ruff standard)
- Use Black for code formatting
- Use Ruff for linting with rules: E, F, I, N, UP, B, C4, SIM, RUF

### Type Hints
- All functions must have type hints
- MyPy strict mode enabled (`disallow_untyped_defs = true`)
- Use `from pathlib import Path` for file paths
- Import typing as needed but prefer built-in types

### Naming Conventions
- Classes: `PascalCase` (e.g., `FrontmatterProcessor`)
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: prefix with underscore (`_method`)

### Imports
- Use `isort`-style imports (handled by Ruff)
- Group: stdlib → third-party → local imports
- Use absolute imports for project modules

### Error Handling
- Use specific exceptions
- Include meaningful error messages
- Handle file operations with context managers
- Gracefully skip invalid files in batch operations

### Testing
- Use `unittest` framework
- Mock external API calls
- Test both success and error paths
- Use descriptive test method names

### Dependencies
- Typer for CLI framework
- python-frontmatter for YAML parsing
- OpenRouter for AI API calls
- pytest for testing with coverage