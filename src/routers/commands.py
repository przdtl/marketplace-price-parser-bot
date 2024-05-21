from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer('Привет **{}**'.format(message.from_user.full_name))


@router.message()
async def other_messages_handler(message: Message) -> None:
    pass
