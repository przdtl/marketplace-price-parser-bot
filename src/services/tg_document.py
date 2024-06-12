import aiohttp

from aiogram.types import (Message, File, FSInputFile)

from src.config import Settings
from src.loader import bot
from src.services.pandas_service import (
    read_first_column_dataframe_from_excel, get_list_of_first_column_dataframe)


async def get_document_from_message(message: Message) -> File:
    '''Получает документ из сообщения'''
    file_id = message.document.file_id
    file = await bot.get_file(file_id)

    return file


async def read_first_column_from_sended_excel_document(message: Message) -> list:
    '''
    Получает из сообщения объект документа и конвертирует данный Excel документ в объект ``pandas`` ``DataFrame``

    Args:
        message (Message): Сообщение Telegram

    Raises:
        ValueError: Если отправленный документ не соответсвует расширению Excel файла

    Returns:
        list: Список элементов, считанных из первого столбца Excel файла
    '''
    document = await get_document_from_message(message)
    path_to_file_in_tg_server = 'https://api.telegram.org/file/bot{}/{}'.format(
        Settings().BOT_TOKEN, document.file_path)
    df = read_first_column_dataframe_from_excel(path_to_file_in_tg_server)
    first_column_items = get_list_of_first_column_dataframe(df)

    return first_column_items


async def get_product_prices_by_articuls(*articuls) -> list[float]:
    '''Отправляет запрос на сервис парсинга с данными о артикулах и возвращает список цен на эти товары'''
    url = Settings().OZON_PRICE_PARSER_SERVICE_URL
    request_body = {
        'articuls': articuls
    }

    prices = []

    async with aiohttp.ClientSession() as session:
        response = await session.post(url, json=request_body)
        json_answer = await response.json()
        prices = json_answer['prices']

    return prices