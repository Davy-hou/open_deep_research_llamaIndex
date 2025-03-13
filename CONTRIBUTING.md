# Contributing to open_deep_research_llamaindex

Thank you for your interest in contributing to open_deep_research_llamaindex! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion for improvement:

1. Check if the issue already exists in the [GitHub Issues](https://github.com/yourusername/open_deep_research_llamaindex/issues)
2. If not, create a new issue with a descriptive title and detailed information about the bug or suggestion

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature or bugfix: `git checkout -b feature/your-feature-name` or `git checkout -b fix/your-bugfix-name`
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Commit your changes with clear, descriptive commit messages
6. Push your branch to your fork
7. Submit a pull request to the main repository

### Development Setup

1. Clone the repository
2. Install development dependencies: `pip install -e ".[dev]"`
3. Copy `.env.example` to `.env` and add your API keys

## Coding Standards

- Follow PEP 8 style guidelines for Python code
- Write docstrings for all functions, classes, and modules
- Include type hints where appropriate
- Write tests for new functionality

## Testing

Before submitting a pull request, make sure all tests pass:

```bash
python -m pytest
```

## Documentation

If you're adding new features or changing existing ones, please update the documentation accordingly.

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).