import os

from aiogram.types import (Message, File, FSInputFile)

from src.settings.loader import bot
from src.settings.config import Settings


def get_excel_filename_by_chat_id(message: Message, is_absolute_path: bool = True) -> str:
    '''Возвращает имя excel файла по id чата, может возвращать полный путь до данного файла'''
    file_name = str(message.chat.id) + '.xlsx'

    return Settings().PATH_TO_EXCEL_FOLDER + file_name if is_absolute_path else file_name


async def get_document_from_message(message: Message) -> File:
    '''Получает документ из сообщения'''
    file_id = message.document.file_id
    file = await bot.get_file(file_id)

    return file


async def download_document_file(path_to_document: str, destination_path_to_file: str) -> str:
    '''Скачивает отправленный пользователем Excel файл на диск и возвращает путь к нему'''

    await bot.download_file(path_to_document, destination_path_to_file)

    return destination_path_to_file


async def check_file_extention_is_excel(path_to_document: str) -> bool:
    '''Проверяет расширение файла на принадлежность к формату Excel'''

    file_name, file_extension = os.path.splitext(path_to_document)

    return file_extension in Settings().ALLOWED_EXCEL_EXTENTIONS


async def download_document_if_extention_is_excel(path_to_document: str, destination_path_to_file: str) -> str:
    '''Скачивает документ если его расшираение пренадлежит формату Excel и возвращает путь к скачанному файлу'''
    if not await check_file_extention_is_excel(path_to_document):
        return ''

    return await download_document_file(path_to_document, destination_path_to_file)


async def get_document_from_message_and_download_if_extention_is_excel(message: Message, destination_path_to_file: str) -> str:
    '''Получает файл из сообщения и скачивает его если расшираение пренадлежит формату Excel и возвращает путь к скачанному файлу'''
    document = await get_document_from_message(message)

    return await download_document_if_extention_is_excel(document.file_path, destination_path_to_file)


async def send_document_if_exists(message: Message, document_path: str, caption: str = '') -> bool:
    '''Отправляет документ если он существует по заданному пути, в зависимости от того, существует ли документ возвращается True или False'''
    if not os.path.exists(document_path):
        return False

    await message.answer_document(document=FSInputFile(document_path), caption=caption)
    return True
