import asyncio
import logging
from alembic.config import Config
from alembic import command
from src.config.config import DATABASE_URL # Requires URL from your config

logger = logging.getLogger(__name__)

# Path to the Alembic configuration file
# Important: the path must be relative to the project root!
ALEMBIC_CONFIG_PATH = "alembic.ini"

def _run_migrations_sync():
    """
    Synchronously executes the 'alembic upgrade head' command.
    This function is intended to be called from an asynchronous environment.
    """
    try:
        # 1. Load the Alembic configuration
        alembic_cfg = Config(ALEMBIC_CONFIG_PATH)
        
        # 2. Pass the database URL so env.py can use it
        alembic_cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
        
        logger.info("Executing 'alembic upgrade head' command...")
        # 3. Execute the migration to the latest version (head)
        command.upgrade(alembic_cfg, "head")
        logger.info("✅ Alembic migrations executed successfully.")

    except Exception as e:
        logger.error(f"❌ Error during Alembic migration execution: {e}", exc_info=True)
        # Re-raise the error for main.py to handle
        raise

async def run_migrations():
    """
    Asynchronously launches the synchronous migration function in a separate thread (executor).
    """
    # Use run_in_executor to run synchronous code in an asynchronous environment
    loop = asyncio.get_event_loop()
    # `None` means we use the default ThreadPoolExecutor
    await loop.run_in_executor(None, _run_migrations_sync)