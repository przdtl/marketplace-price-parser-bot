import aiohttp
import hashlib

from aiogram.types import Message, File
from aiogram.types.input_file import BufferedInputFile

from src.config import Settings
from src.loader import bot
from src.services.pandas_service import (
    read_first_column_dataframe_from_excel,
    read_first_column_dataframe_from_csv,
    get_list_of_first_column_dataframe,
    get_table_of_articuls_and_its_prices,
    get_excel_bytestr_from_dataframe,
    get_csv_bytestr_from_dataframe
)
from src.services.mongo import (
    add_list_of_products_in_document
)


async def get_document_from_message(message: Message) -> File:
    '''Получает документ из сообщения'''
    file_id = message.document.file_id
    file = await bot.get_file(file_id)

    return file


async def read_first_column_from_sended_excel_document(message: Message) -> list[int]:
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
        Settings().BOT_TOKEN, document.file_path
    )
    df = read_first_column_dataframe_from_excel(path_to_file_in_tg_server)
    first_column_items = get_list_of_first_column_dataframe(df)

    return first_column_items


async def read_first_column_from_sended_csv_document(message: Message) -> list[int]:
    document = await get_document_from_message(message)
    path_to_file_in_tg_server = 'https://api.telegram.org/file/bot{}/{}'.format(
        Settings().BOT_TOKEN, document.file_path
    )
    df = read_first_column_dataframe_from_csv(path_to_file_in_tg_server)
    first_column_items = get_list_of_first_column_dataframe(df)

    return first_column_items


async def send_excel_with_products_info(message: Message, marketplace_name: str) -> None:
    df = await get_table_of_articuls_and_its_prices(chat_id=message.chat.id, marketplace_name=marketplace_name)
    excel_bytes = get_excel_bytestr_from_dataframe(df)
    document_filename = hashlib.md5(excel_bytes).hexdigest()[:7] + '.xlsx'
    excel_buffered_file = BufferedInputFile(excel_bytes, document_filename)
    await bot.send_document(
        chat_id=message.chat.id,
        document=excel_buffered_file,
    )


async def send_csv_with_products_info(message: Message, marketplace_name: str) -> None:
    df = await get_table_of_articuls_and_its_prices(chat_id=message.chat.id, marketplace_name=marketplace_name)
    csv_bytes = get_csv_bytestr_from_dataframe(df)
    document_filename = hashlib.md5(csv_bytes).hexdigest()[:7] + '.xlsx'
    csv_buffered_file = BufferedInputFile(csv_bytes, document_filename)
    await bot.send_document(
        chat_id=message.chat.id,
        document=csv_buffered_file,
    )


async def write_articuls_from_excel_in_db(message: Message, marketplace_name: str) -> None:
    try:
        articuls_list = await read_first_column_from_sended_excel_document(message)
    except ValueError as e:
        if "Excel file format cannot be determined" in str(e):
            await message.answer('Вы передали файл с неверным расширением!')
    else:
        await add_list_of_products_in_document(
            chat_id=message.chat.id,
            marketplace_name=marketplace_name,
            articuls=articuls_list
        )


async def write_articuls_from_csv_in_db(message: Message, marketplace_name: str) -> None:
    articuls_list = await read_first_column_from_sended_csv_document(message)
    await add_list_of_products_in_document(
        chat_id=message.chat.id,
        marketplace_name=marketplace_name,
        articuls=articuls_list
    )

# async def get_product_prices_by_articuls(*articuls) -> list[float]:
#     '''Отправляет запрос на сервис парсинга с данными о артикулах и возвращает список цен на эти товары'''
#     url = Settings().OZON_PRICE_PARSER_SERVICE_URL
#     request_body = {
#         'articuls': articuls
#     }

#     prices = []

#     async with aiohttp.ClientSession() as session:
#         response = await session.post(url, json=request_body)
#         json_answer = await response.json()
#         prices = json_answer['prices']

#     return prices
