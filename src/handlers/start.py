from aiogram import types
from aiogram.filters import CommandStart
from aiogram import Dispatcher

async def command_start_handler(message: types.Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")

def register_start_handler(dp: Dispatcher):
    dp.message.register(command_start_handler, CommandStart())
