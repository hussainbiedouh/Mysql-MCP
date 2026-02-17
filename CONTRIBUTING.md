# Contributing to MySQL MCP

Thank you for your interest in contributing to MySQL MCP! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- MySQL server (for integration testing)
- UV package manager or pip
- Git

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mysql-mcp.git
   cd mysql-mcp
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/original/mysql-mcp.git
   ```

## Development Setup

```bash
# Create virtual environment
uv venv

# Install in development mode with all dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

## Making Changes

### Branch Naming

Create a branch for your changes:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
# or
git checkout -b docs/your-documentation-update
```

### Commit Messages

Follow conventional commit format:

- `feat: add new feature`
- `fix: resolve bug in query execution`
- `docs: update README examples`
- `test: add tests for connection handling`
- `refactor: simplify JSON conversion logic`
- `chore: update dependencies`

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_utils.py -v

# Run with coverage
python -m pytest tests/ -v --cov=mysql_mcp --cov-report=term-missing
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Use descriptive test function names
- Include edge cases and error handling

Example:
```python
def test_query_with_invalid_database():
    """Test that query returns error for non-existent database."""
    result = query(
        host="localhost",
        port=3306,
        username="root",
        password="secret",
        database="nonexistent_db",
        query="SELECT 1"
    )
    assert result["success"] is False
    assert "error" in result
```

### Integration Testing

For integration tests requiring a MySQL server:

1. Set up a test MySQL database
2. Use environment variables for credentials:
   ```bash
   export MYSQL_TEST_HOST=localhost
   export MYSQL_TEST_PORT=3306
   export MYSQL_TEST_USER=test_user
   export MYSQL_TEST_PASSWORD=test_password
   ```

## Submitting Changes

### Pull Request Process

1. **Update your branch** with upstream:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests** to ensure everything passes:
   ```bash
   python -m pytest tests/ -v
   ruff check src/
   mypy src/
   ```

3. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request** on GitHub with:
   - Clear title and description
   - Reference to any related issues
   - List of changes made
   - Screenshots (if applicable)

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated (if needed)
- [ ] CHANGELOG.md updated (if needed)
- [ ] Commit messages follow conventional format

## Coding Standards

### Python Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines
- Maximum line length: 100 characters
- Use type hints for all function signatures
- Write docstrings for all public functions

### Code Quality Tools

```bash
# Lint code
ruff check src/

# Format code
ruff format src/

# Type check
mypy src/
```

### Documentation

- Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> dict[str, Any]:
    """
    Short description of function.

    Longer description if needed.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When param1 is empty.
    """
```

### Type Annotations

Always use type annotations:

```python
from typing import Any

def connect(
    host: str,
    port: int,
    username: str,
    password: str,
    database: str | None = None
) -> dict[str, Any]:
    ...
```

## Project Structure

Maintain the following structure:

```
mysql-mcp/
├── src/mysql_mcp/     # Source code
│   ├── __init__.py
│   ├── server.py      # MCP server
│   └── utils.py       # Utilities
├── tests/             # Test files
├── mcp-configs/       # MCP client configs
├── docs/              # Additional docs
└── examples/          # Usage examples
```

## Getting Help

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues before creating new ones

Thank you for contributing!