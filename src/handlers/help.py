# src/handlers/help.py
from aiogram import Router, types
from aiogram.filters import Command

router = Router()  # Create router

@router.message(Command("help"))
async def command_help_handler(message: types.Message) -> None:
    await message.answer("I can help you with many things. Use /start to begin.")
