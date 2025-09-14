import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from src.config.config import BOT_TOKEN
from src.handlers import register_all_handlers

# Create a Dispatcher instance
dp = Dispatcher()

# Register all handlers
register_all_handlers(dp)

# Main asynchronous function to start the bot
async def main():
    # Initialize the Bot
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    logging.info("🤖 Bot is starting...")

    try:
        # Start long polling
        await dp.start_polling(bot)
    except Exception as e:
        logging.error("❌ Unexpected error during bot polling:", exc_info=e)
    finally:
        # Close the bot's session on shutdown
        await bot.session.close()
        logging.info("🛑 Bot stopped gracefully.")

# Entry point of the program
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("🔌 Bot shutdown via KeyboardInterrupt/SystemExit")
