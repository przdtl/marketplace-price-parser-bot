from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.keyboards import main_manu_keyboard


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer('Привет **{}**'.format(message.from_user.full_name), reply_markup=main_manu_keyboard())


@router.message()
async def all_other_messages_handler(message: Message) -> None:
    await message.answer('Я не знаю такой команды!')
