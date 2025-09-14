from aiogram import types
from aiogram.filters import Command
from aiogram import Dispatcher

def register_help_handler(dp: Dispatcher) -> None:
    """Register /help command handler."""
    
    @dp.message(Command("help"))
    async def command_help_handler(message: types.Message) -> None:
        await message.answer("I can help you with many things. Use /start to begin.")
