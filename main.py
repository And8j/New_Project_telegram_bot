import asyncio
import logging
import sys
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variables
TOKEN = getenv("BOT_TOKEN")

# Check if the token is set
if not TOKEN:
    print("❌ BOT_TOKEN not set in .env file or environment variables.")
    sys.exit(1)

# Create a Dispatcher instance
dp = Dispatcher()

# --- Handlers section ---
# Handler for the /start command
@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")

# Handler for the /help command
@dp.message(Command("help"))
async def command_help_handler(message: types.Message) -> None:
    await message.answer("I can help you with many things.")

# --- End of handlers section ---

# Main asynchronous function to start the bot
async def main():
    # Initialize the Bot
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    logging.info("🤖 Bot is starting...")

    try:
        # Start long polling
        await dp.start_polling(bot)
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
