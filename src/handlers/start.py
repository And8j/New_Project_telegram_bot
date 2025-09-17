# src/handlers/start.py
from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()  # create router

@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")
