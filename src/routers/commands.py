from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

# from src.services.tg_document import (
#     get_document_from_message_and_download_if_extention_is_excel,
#     send_document_if_exists,
#     get_excel_filename_by_chat_id
# )
from src.keyboards import main_manu_keyboard


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer('Привет **{}**'.format(message.from_user.full_name), reply_markup=main_manu_keyboard())


# @router.message(F.document)
# async def documnets_messages_handler(message: Message) -> None:

#     path_to_excel_document = await get_document_from_message_and_download_if_extention_is_excel(
#         message=message,
#         destination_file_name=get_excel_filename_by_chat_id(message)
#     )
#     await message.answer('Файл успешно сохранён!' if path_to_excel_document else 'Ошибка файла!')


@router.message()
async def all_other_messages_handler(message: Message) -> None:
    await message.answer('Я не знаю такой команды!')
