
import os
import aiohttp

from aiogram.types import (Message, File, FSInputFile)

from src.settings.config import Settings
from src.settings.loader import bot


def get_excel_filename_by_chat_id(message: Message, is_absolute_path: bool = True) -> str:
    '''Возвращает имя excel файла по id чата, может возвращать полный путь до данного файла'''
    file_name = str(message.chat.id) + '.xlsx'

    return Settings().PATH_TO_EXCEL_FOLDER + file_name if is_absolute_path else file_name


def check_if_excel_by_chat_id_exists(message: Message) -> bool:
    path_to_document = get_excel_filename_by_chat_id(message)

    return os.path.exists(path_to_document)


async def get_document_from_message(message: Message) -> File:
    '''Получает документ из сообщения'''
    file_id = message.document.file_id
    file = await bot.get_file(file_id)

    return file


async def download_document_file(path_to_document: str, destination_path_to_file: str) -> str:
    '''Скачивает отправленный пользователем Excel файл на диск и возвращает путь к нему'''

    await bot.download_file(path_to_document, destination_path_to_file)

    return destination_path_to_file


def check_file_extention_is_excel(path_to_document: str) -> bool:
    '''Проверяет расширение файла на принадлежность к формату Excel'''

    file_name, file_extension = os.path.splitext(path_to_document)

    return file_extension in Settings().ALLOWED_EXCEL_EXTENTIONS


async def download_document_if_extention_is_excel(path_to_document: str, destination_path_to_file: str) -> str:
    '''Скачивает документ если его расшираение пренадлежит формату Excel и возвращает путь к скачанному файлу'''
    if not check_file_extention_is_excel(path_to_document):
        return ''

    return await download_document_file(path_to_document, destination_path_to_file)


async def get_document_from_message_and_download_if_extention_is_excel(message: Message) -> str:
    '''Получает файл из сообщения и скачивает его если расшираение пренадлежит формату Excel и возвращает путь к скачанному файлу'''
    destination_path_to_file = get_excel_filename_by_chat_id(message)
    document = await get_document_from_message(message)

    return await download_document_if_extention_is_excel(document.file_path, destination_path_to_file)


async def send_document_if_exists(message: Message, document_path: str, caption: str = '') -> None:
    '''Отправляет документ если он существует по заданному пути, в зависимости от того, существует ли документ возвращается True или False'''
    if check_if_excel_by_chat_id_exists(message):
        await message.answer_document(document=FSInputFile(document_path), caption=caption)


async def send_document_by_chat_id(message: Message, caption: str = '') -> None:
    destination_path_to_file = get_excel_filename_by_chat_id(message)
    await send_document_if_exists(message, destination_path_to_file, caption)


async def get_product_prices_by_articuls(*articuls) -> list[float]:
    '''Отправляет запрос на сервис парсинга с данными о артикулах и возвращает список цен на эти товары'''
    url = 'http://127.0.0.1:8000/price/'
    request_body = {
        'articuls': articuls
    }

    prices = []

    async with aiohttp.ClientSession() as session:
        response = await session.post(url, json=request_body)
        json_answer = await response.json()
        prices = json_answer['prices']

    return prices
