from aiogram.types import Message

from src.settings.loader import bot
from src.settings.config import Settings


async def download_excel_file(message: Message) -> str:
    '''Скачивает отправленный пользователем Excel файл на диск и возвращает путь к нему'''

    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    file_name = str(message.chat.id) + '.xls'

    await bot.download_file(file_path, file_name)

    return Settings().PATH_TO_EXCEL_FOLDER + '/' + file_name
