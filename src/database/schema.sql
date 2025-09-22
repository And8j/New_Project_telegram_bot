-- Database schema for the financial assistant Telegram bot (normalized version).

-- Table to store information about bot users.
CREATE TABLE users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id     BIGINT NOT NULL UNIQUE,
    full_name       TEXT NOT NULL,
    username        TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store expense/income categories created by users.
CREATE TABLE categories (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    name            TEXT NOT NULL COLLATE NOCASE,
    description     TEXT,
    -- Ensures category names are unique per user (case-insensitive).
    UNIQUE(user_id, name),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Table to store types of transactions (expense, income, transfer, etc.).
CREATE TABLE transaction_types (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL UNIQUE COLLATE NOCASE,
    icon            TEXT  -- Optional: emoji or icon name
);

-- Table to log each individual expense/income.
CREATE TABLE expenses (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    category_id     INTEGER,
    type_id         INTEGER NOT NULL,
    amount          REAL NOT NULL,
    currency        TEXT CHECK (LENGTH(currency) = 3) DEFAULT 'USD',
    description     TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (type_id) REFERENCES transaction_types(id)
);

-- Optional table to store default categories for new users.
CREATE TABLE default_categories (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL UNIQUE COLLATE NOCASE
);

-- Indexes for performance optimization.
CREATE INDEX idx_expenses_created_at ON expenses (created_at);
CREATE INDEX idx_expenses_user_id ON expenses (user_id);
CREATE INDEX idx_categories_user_id ON categories (user_id);
