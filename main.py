import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from src.config.config import BOT_TOKEN
from src.handlers import router 

# Configure logging once at the very beginning
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

dp = Dispatcher()
dp.include_router(router)

# Main asynchronous function to start the bot
async def main():
    """
    Main entry point for the bot application.
    Initializes the database and starts the bot polling.
    """
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
