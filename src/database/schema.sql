-- Database schema for the financial assistant Telegram bot (PostgreSQL version).

-- Table to store information about bot users.
CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    telegram_id     BIGINT NOT NULL UNIQUE,
    full_name       TEXT NOT NULL,
    username        TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Table to store expense/income categories created by users.
CREATE TABLE categories (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL,
    name            TEXT NOT NULL,
    description     TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Ensures category names are unique per user (case-insensitive).
CREATE UNIQUE INDEX idx_categories_user_id_lower_name_unique ON categories (user_id, lower(name));


-- Table to store types of transactions (expense, income, transfer, etc.).
CREATE TABLE transaction_types (
    id              SERIAL PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    icon            TEXT  -- Optional: emoji or icon name
);

-- Table to log each individual expense/income.
CREATE TABLE expenses (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL,
    category_id     INTEGER,
    type_id         INTEGER NOT NULL,
    amount          NUMERIC(10, 2) NOT NULL,
    currency        TEXT CHECK (LENGTH(currency) = 3) DEFAULT 'USD',
    description     TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (type_id) REFERENCES transaction_types(id)
);

-- Optional table to store default categories for new users.
CREATE TABLE default_categories (
    id              SERIAL PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE
);

-- Indexes for performance optimization.
CREATE INDEX idx_expenses_created_at ON expenses (created_at);
CREATE INDEX idx_expenses_user_id ON expenses (user_id);
CREATE INDEX idx_categories_user_id ON categories (user_id);