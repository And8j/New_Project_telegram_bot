import logging
import os
import sys


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager

from src.models.base import Base
# Import all models and relationships to ensure they are registered with SQLAlchemy's metadata
from src.models.user import User
from src.models.category import Category, DefaultCategory
from src.models.transaction import Expense, TransactionType
from src.models import relationships

# Configure logging
logger = logging.getLogger(__name__)

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
