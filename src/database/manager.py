import logging
import os
import sys


from sqlalchemy import (
    create_engine, Column, Integer, BigInteger, Text, Numeric,
    DateTime, ForeignKey, Index
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager

# Configure logging
logger = logging.getLogger(__name__)

# Base class for your SQLAlchemy ORM models
# SELECT * FROM users;
# ['1, 1234, john, johnny, 2025-01-01 12:00:00+00']
Base = declarative_base()

class User(Base):
    """
    Represents a user in the system, typically a Telegram user.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True) # Unique identifier for the user (SERIAL)
    telegram_id = Column(BigInteger, nullable=False, unique=True) # Telegram user ID, must be unique
    full_name = Column(Text, nullable=False) # User's full name
    username = Column(Text) # User's Telegram username (optional)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Timestamp of user creation (TIMESTAMPTZ DEFAULT NOW())

    # Relationships:
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, full_name='{self.full_name}')>"

class Category(Base):
    """
    Represents an expense/income category belonging to a specific user.
    """
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True) # Unique identifier for the category (SERIAL)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False) # Foreign key to the User table. If user is deleted, categories are deleted.
    name = Column(Text, nullable=False) # Name of the category
    description = Column(Text) # Optional description for the category

    # Relationship:
    user = relationship("User", back_populates="categories")
    expenses = relationship("Expense", back_populates="category", cascade="all, delete-orphan")

    # Table arguments for unique constraints and indexes:
    __table_args__ = (
        Index('idx_categories_user_id_lower_name_unique', user_id, func.lower(name), unique=True), 
    )

    def __repr__(self):
        return f"<Category(id={self.id}, user_id={self.user_id}, name='{self.name}')>"

class TransactionType(Base):
    """
    Represents the type of a financial transaction (e.g., expense, income, transfer).
    These are typically predefined and not user-specific.
    """
    __tablename__ = 'transaction_types'
    id = Column(Integer, primary_key=True, autoincrement=True) # Unique identifier for the transaction type (SERIAL)
    name = Column(Text, nullable=False, unique=True) # Name of the transaction type (e.g., 'expense', 'income'), must be unique
    icon = Column(Text) # Optional icon (e.g., emoji) for the transaction type

    # Relationship:
    expenses = relationship("Expense", back_populates="type")

    def __repr__(self):
        return f"<TransactionType(id={self.id}, name='{self.name}')>"

class Expense(Base):
    """
    Represents a single financial transaction (expense or income).
    """
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, autoincrement=True) # Unique identifier for the expense (SERIAL)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False) # Foreign key to the User table. If user is deleted, expenses are deleted.
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL')) # Foreign key to the Category table. If category is deleted, this field is set to NULL.
    type_id = Column(Integer, ForeignKey('transaction_types.id'), nullable=False) # Foreign key to TransactionType, cannot be NULL.
    amount = Column(Numeric(10, 2), nullable=False) # Amount of the transaction with 10 total digits and 2 decimal places.
    currency = Column(Text, default='USD') # Currency code (e.g., 'USD', 'EUR'), defaults to 'USD'
    description = Column(Text) # Optional description for the expense
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Timestamp of expense creation (TIMESTAMPTZ DEFAULT NOW())

    # Relationships:
    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")
    type = relationship("TransactionType", back_populates="expenses")

    # Indexes for performance:
    __table_args__ = (
        Index('idx_expenses_created_at', created_at),
        Index('idx_expenses_user_id', user_id),
    )

    def __repr__(self):
        return f"<Expense(id={self.id}, user_id={self.user_id}, amount={self.amount}, type='{self.type.name if self.type else 'N/A'}')>"

class DefaultCategory(Base):
    """
    Represents a predefined default category that can be offered to new users.
    These are global categories, not tied to a specific user initially.
    """
    __tablename__ = 'default_categories'
    id = Column(Integer, primary_key=True, autoincrement=True) # Unique identifier for the default category (SERIAL)
    name = Column(Text, nullable=False, unique=True) # Name of the default category, must be unique

    def __repr__(self):
        return f"<DefaultCategory(id={self.id}, name='{self.name}')>"

# --- DatabaseManager Class ---

class DatabaseManager:
    """
    Manages the SQLAlchemy engine and session factory, and provides methods
    for database initialization and session handling.
    """
    def __init__(self, db_url: str, pool_size: int = 10, max_overflow: int = 20):
        self.db_url = db_url
        self.engine = create_engine(
            db_url,
            echo=False,  # Set to True to see all SQL queries in the console
            pool_size=pool_size, # Number of connections to keep open in the pool
            max_overflow=max_overflow, # Number of connections that can be opened beyond pool_size
            pool_recycle=3600, # Recycle connections after 1 hour (prevent stale connections)
            pool_pre_ping=True # Test connections for liveness before use
        )
        self.Session = sessionmaker(bind=self.engine) # Factory for creating new session objects
        logger.info(f"✅ SQLAlchemy Engine created for {self.db_url}")

    def init_database(self):
        """
        Initializes the database by creating all tables defined in the ORM models
        if they do not already exist.
        """
        logger.info("⏳ Initializing database using SQLAlchemy ORM Base.metadata...")
        try:
            Base.metadata.create_all(self.engine)
            logger.info("✅ Database tables created via ORM Base.metadata.")
        except SQLAlchemyError as e:
            logger.error(f"❌ Error creating tables via ORM Base.metadata: {e}", exc_info=True)
            raise

    @contextmanager
    def get_session(self):
        """
        Provides a transactional SQLAlchemy ORM session via a context manager.
        Ensures proper session lifecycle management (commit, rollback, close).
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e: # Явно вказуємо 'as e' для логування, якщо це потрібно
            session.rollback()
            logger.error(f"❌ Database session rolled back due to error: {e}", exc_info=True)
            raise
        finally:
            session.close()

    def close_all_connections(self):
        """
        Disposes of all connections in the connection pool, closing them.
        Should be called when the application is shutting down.
        """
        self.engine.dispose()
        logger.info("🔌 All SQLAlchemy connections disposed.")

# --- DatabaseManager Initialization and Initial Data Functions ---

# Database connection URL, now fetched from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.critical("❌ Error: DATABASE_URL environment variable is not set. Please check your .env file or environment configuration.")
    sys.exit(1) # Exit if the critical variable is missing

# Initialization happens here, при імпорті модуля
db_manager = DatabaseManager(DATABASE_URL)

