# 🧑‍💻 Contributing Guidelines

Thank you for considering contributing to this project!  
This document provides a set of guidelines and best practices for making contributions.

---

## 🚀 Getting Started

1. **Fork** the repository.
2. **Clone** your fork locally:

```bash
git clone https://github.com/And8j/New_Project_telegram_bot.git
cd New_Project_telegram_bot
```

**🧩 Environment Setup**:  

   We recommend using [`uv`](https://github.com/astral-sh/uv) — a modern, fast Python package and environment manager that replaces `venv` and `pip`.  
   
3. **Install `uv`:**

```bash
pip install pipx
pipx install uv
```
4. **Create and activate virtual environment:**
```
uv venv
```
5. **Install dependencies:**
```
  uv pip install -r requirements.txt
```
6. **(Optional) Compile a clean requirements.txt:**
```
uv pip compile -o requirements.txt
```
7. **Create a new branch for your feature or fix:**
```
git checkout -b feature/your-feature-name
```
## 🛠️ Code Style

Please follow the PEP 8 Python style guide.  
We recommend using the following tools:  
- **Black** for code formatting
- **flake8** for linting
- **isort** for import sorting  

You can install them via:  
```
pip install black flake8 isort
```
To auto-format your code before committing:  
```
black .
isort .
flake8 .
```
## 🧪 Testing
Before submitting any code, make sure tests pass.  

If tests are available, run:
```
pytest
```
If no test suite is available yet, ensure your code runs without errors and doesn't break existing features.  

## ✅ Commit Messages
Use clear and descriptive commit messages. Follow Conventional Commits format:  
Examples:  
```
feat: add new command handler for expense tracking
fix: correct database connection error
docs: update README with environment variables
```
## 🔀 Pull Requests
- Submit PRs to the main or dev branch unless instructed otherwise.  
- Provide a clear description of the changes you made.  
- Link related issues (if any).  
- Make sure your code is clean, formatted, and tested before submitting.
## 📂 Project Structure (Example)
```
project/
│
├── bot/                        # Entry point for the Telegram bot (main.py)
│
├── src/                        # Main application logic
│   ├── config/                 # Configuration and environment variables
│   ├── handlers/               # Telegram message handlers
│   ├── models/                 # Pydantic or ORM models
│   ├── repositories/           # Data access layer
│   ├── services/               # Business logic and services
│   └── utils/                  # Utility functions and helpers
│
├── tests/                      # Unit and integration tests
│
├── .github/                    # GitHub-specific files (e.g. PR templates)
│   └── pull_request_template.md
│
├── .gitignore                  # Git ignore rules
└── CONTRIBUTING.md             # Contribution guidelines
```
⚠️ .venv/ is created by uv venv and should be excluded from Git using .gitignore.  

### Thank You
Your contributions are highly appreciated!  
Feel free to open an issue if you have questions or ideas.

