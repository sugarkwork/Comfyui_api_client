# Contributing to ComfyUI Client

Thank you for your interest in contributing to ComfyUI Client! We welcome contributions from the community.

## How to Contribute

### Reporting Issues

- Use the [GitHub issue tracker](https://github.com/sugarkwork/Comfyui_api_client/issues)
- Check if the issue already exists before creating a new one
- Provide detailed information about the issue:
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - System information

### Submitting Pull Requests

1. Fork the repository
2. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Add tests for new functionality
5. Run the test suite:
   ```bash
   pytest tests/
   ```
6. Format your code:
   ```bash
   black comfyuiclient tests
   isort comfyuiclient tests
   ```
7. Run linting:
   ```bash
   flake8 comfyuiclient tests
   mypy comfyuiclient
   ```
8. Commit your changes with a descriptive message
9. Push to your fork and submit a pull request

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sugarkwork/Comfyui_api_client.git
   cd Comfyui_api_client
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting
- Use isort for import sorting
- Maximum line length is 88 characters
- Write descriptive docstrings for all public functions and classes

### Testing

- Write tests for all new functionality
- Ensure all tests pass before submitting PR
- Aim for high test coverage
- Use pytest for testing

### Documentation

- Update documentation for new features
- Include docstrings in your code
- Update README if necessary
- Add examples for new functionality

## Code of Conduct

Please note that this project follows a Code of Conduct. By participating, you are expected to uphold this code.

## Questions?

If you have questions, please open an issue on GitHub or reach out to the maintainers.

Thank you for contributing!