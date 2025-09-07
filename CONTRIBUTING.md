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

3. **Create a virtual environment and activate it**:
```
python3 -m venv venv
source venv/bin/activate  # For Unix/macOS
# OR
venv\Scripts\activate     # For Windows
```
4. **Install dependencies:**
```
pip install -r requirements.txt
```
5. **Create a new branch for your feature or fix:**
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
├── bot/                # Telegram bot logic
├── database/           # Database models and connection
├── config/             # Environment/configuration settings
├── tests/              # Unit and integration tests
├── requirements.txt    # Python dependencies
├── .env.example        # Example of required environment variables
├── README.md
└── CONTRIBUTING.md
```
### Thank You
Your contributions are highly appreciated!  
Feel free to open an issue if you have questions or ideas.

