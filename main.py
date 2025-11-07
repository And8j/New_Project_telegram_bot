import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from src.config.config import BOT_TOKEN
from src.handlers import router 
from src.database.manager import setup_initial_data
from src.database.migrations import run_migrations
from sqlalchemy.exc import SQLAlchemyError

# Configure logging once at the very beginning
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Maximum number of retries for database connection
MAX_RETRIES = 10
RETRY_DELAY_SECONDS = 2 

dp = Dispatcher()
dp.include_router(router)

async def initialize_database_with_retries():
    """
    Asynchronously initializes the database with retry logic and exponential backoff.
    Raises an exception if the maximum number of retries is reached.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Attempt {attempt}/{MAX_RETRIES}: launching migrations Alembic...")
            # Run database migrations
            await run_migrations()
            logger.info("✅ migrations completed successfully.")
            # Adding initial data
            await setup_initial_data()
            logger.info("✅ database successfully initialized.")
            return # Successfully connected and initialized
        except SQLAlchemyError as e:
            # Connecting to the migrations failed
            logger.error(f"❌ Attempt {attempt}/{MAX_RETRIES}: Attempt connection to migrations failed. Error: {e.__class__.__name__} - {e}")

            # If we've reached the max attempts, re-raise the exception
            if attempt == MAX_RETRIES:
                logger.critical("🚨 Maximum attempts to connect to migrations reached. Exiting")
                raise # Re-raise the original exception
            
            # To count the wait time before the next retry (exponential backoff, max 30 seconds)
            wait_time = min(RETRY_DELAY_SECONDS * (2 ** (attempt - 1)), 30)
                
            logger.info(f"⏳ wait {wait_time} seconds before the next attempt...")
            # Use asyncio.sleep for non-blocking wait
            await asyncio.sleep(wait_time)

# Main asynchronous function to start the bot
async def main():
    """
    Main entry point for the bot application.
    Initializes the database and starts the bot polling.
    """
    try:
        # Initialization of Database with retries
        # await initialize_database_with_retries()
        setup_initial_data()
    except Exception as e: # Catching a general exception if DB init fails
        logger.error("❌ Failed to initialize database, exiting.", exc_info=e)
        sys.exit(1) # Important: stop the bot if the DB is not ready

    # Initialize the Bot
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    logger.info("🤖 Bot is starting...")

    try:
        # Start long polling
        await dp.start_polling(bot)
    except Exception as e: # Catching general exceptions during bot polling
        logger.error("❌ Unexpected error during bot polling:", exc_info=e)
    finally:
        # Close the bot's session on shutdown
        await bot.session.close()
        logger.info("🛑 Bot stopped gracefully.")

# Entry point of the program
if __name__ == "__main__":
    # The basicConfig for logging is now at the top of the file, removed from here.
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("🔌 Bot shutdown via KeyboardInterrupt/SystemExit")
    except Exception as e:
        logger.critical(f"❌ An unhandled error occurred: {e}", exc_info=e)
        sys.exit(1)
