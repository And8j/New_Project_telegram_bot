# AGENTS.md

This file provides guidance for AI coding agents working on this project.

## Project Overview

This project is a Telegram bot built using the `aiogram` library. The bot's functionality is defined in the `src` directory, with `main.py` as the entry point.

## Setup commands

This project uses `uv` for package and environment management.

```bash
# Install uv (if you don't have it)
pip install pipx
pipx install uv

# Create and activate the virtual environment
uv venv

# Install dependencies
uv pip install -r requirements.txt

# Run the main application
python main.py
```

## Docker

This project includes a `Dockerfile` and `docker-compose.yml` for containerization.

To build and run the application using Docker Compose:

```bash
# Build the Docker images
docker-compose build

# Start the services in the background
docker-compose up -d
```

## Code style

The project enforces a consistent code style using the following tools:
*   **Black** for code formatting
*   **flake8** for linting
*   **isort** for import sorting

Before committing, please format your code:
```bash
black .
isort .
flake8 .
```

## Testing instructions

The project uses `pytest` for testing. Tests are located in the `tests/` directory.

To run all tests:
```bash
pytest
```
Ensure all existing tests pass before submitting a pull request.

## PR instructions

Please follow the guidelines in `CONTRIBUTING.md` and the pull request template. Key points include:

*   **Commit Messages**: Use the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format (e.g., `feat: ...`, `fix: ...`).
*   **Branch Naming**: Use descriptive branch names like `feature/your-feature-name` or `fix/bug-report`.
*   **Code Quality**: Ensure your code is formatted, linted, and passes all tests before submission.

## Security considerations

*   Sensitive data, such as the bot token, should be stored in a `.env` file and not committed to version control. Use the `.env.example` file in `src/handlers/` as a template.
*   Be mindful of potential vulnerabilities when handling user input.

## Extra instructions

*   The project structure is organized into modules within the `src/` directory. Please maintain this structure when adding new features.
*   Configuration is handled in the `src/config/` directory.
