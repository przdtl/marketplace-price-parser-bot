import hashlib

from typing import Any

from aiogram.types import Message, File
from aiogram.types.input_file import BufferedInputFile

from src.config import Settings
from src.loader import bot
from src.enums import (
    ExtendOrReplaceArticulsEnum,
    ProductsInfoExportWayEnum
)
from src.services.pandas_service import (
    read_first_column_dataframe_from_excel,
    read_first_column_dataframe_from_csv,
    get_list_of_first_column_dataframe,
    get_table_of_articuls_and_its_prices,
    get_excel_bytestr_from_dataframe,
    get_csv_bytestr_from_dataframe
)
from src.services.mongo import (
    add_list_of_products_in_document,
    delete_all_products_from_user_in_specific_marketplace
)


async def get_document_from_message(message: Message) -> File:
    '''Получает документ из сообщения'''
    file_id = message.document.file_id
    file = await bot.get_file(file_id)

    return file


async def read_first_column_from_sended_excel_document(message: Message) -> list[int]:
    '''
    Получает из сообщения объект документа и конвертирует данный Excel документ в объект ``pandas`` ``DataFrame``

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
    '''
    Получает из сообщения объект документа и конвертирует данный CSV документ в объект ``pandas`` ``DataFrame``

    Raises:
        ValueError: Если отправленный документ не соответсвует расширению CSV файла

    Returns:
        list: Список элементов, считанных из первого столбца CSV файла
    '''
    document = await get_document_from_message(message)
    path_to_file_in_tg_server = 'https://api.telegram.org/file/bot{}/{}'.format(
        Settings().BOT_TOKEN, document.file_path
    )
    df = read_first_column_dataframe_from_csv(path_to_file_in_tg_server)
    first_column_items = get_list_of_first_column_dataframe(df)

    return first_column_items


async def send_excel_with_products_info(message: Message, marketplace_name: str) -> None:
    '''
    Отправляет ползователю информацию о товарах с конкретного паркетплейса в формате Excel

    Raises:
        ValueError: Если пользователь не заносил информацию о товарах с этого маркетплейса (информация отсуствует)

    '''
    df = await get_table_of_articuls_and_its_prices(chat_id=message.chat.id, marketplace_name=marketplace_name)
    excel_bytes = get_excel_bytestr_from_dataframe(df)

    if df.empty:
        raise ValueError('The document cannot be empty!')

    document_filename = hashlib.md5(excel_bytes).hexdigest()[:7] + '.xlsx'
    excel_buffered_file = BufferedInputFile(excel_bytes, document_filename)
    await bot.send_document(
        chat_id=message.chat.id,
        document=excel_buffered_file,
    )


async def send_csv_with_products_info(message: Message, marketplace_name: str) -> None:
    '''
    Отправляет ползователю информацию о товарах с конкретного паркетплейса в формате CSV

    Raises:
        ValueError: Если пользователь не заносил информацию о товарах с этого маркетплейса (информация отсуствует)

    '''
    df = await get_table_of_articuls_and_its_prices(chat_id=message.chat.id, marketplace_name=marketplace_name)
    csv_bytes = get_csv_bytestr_from_dataframe(df)

    if df.empty:
        raise ValueError('The document cannot be empty!')

    document_filename = hashlib.md5(csv_bytes).hexdigest()[:7] + '.csv'
    csv_buffered_file = BufferedInputFile(csv_bytes, document_filename)
    await bot.send_document(
        chat_id=message.chat.id,
        document=csv_buffered_file,
    )


async def get_list_of_articuls_from_message_document(message: Message) -> list[int]:
    '''Возвращает список артикулов, считанных из отправленного документа. Валидные типы: Excel и CSV'''
    try:
        return await read_first_column_from_sended_excel_document(message)
    except ValueError:
        pass
    try:
        return await read_first_column_from_sended_csv_document(message)
    except ValueError as e:
        print(e)
        raise ValueError('The document has an invalid extension')


async def write_articuls_in_db(message: Message, answer_option: str, state_data: dict[str, Any]) -> None:
    '''Записывает артикулы товаров в БД. Присутствует выбор добавления артикулов к уже существующим или полная замена старых на новые'''
    marketplace_name = state_data.get('marketplace_name')
    articuls_list = state_data.get('articuls')

    if answer_option == ExtendOrReplaceArticulsEnum.REPLACE.value:
        await delete_all_products_from_user_in_specific_marketplace(
            chat_id=message.chat.id,
            marketplace_name=marketplace_name,
        )

    await add_list_of_products_in_document(
        chat_id=message.chat.id,
        marketplace_name=marketplace_name,
        articuls=articuls_list
    )


async def send_products_info(message: Message, marketplace_name: str, export_way: str) -> None:
    '''Отправляет пользователю информацию о товарах в зависимости от желаемого способа экспорта (excel, csv, ...)'''
    match export_way:
        case ProductsInfoExportWayEnum.EXCEL.value:
            await send_excel_with_products_info(message, marketplace_name)
        case ProductsInfoExportWayEnum.CSV.value:
            await send_csv_with_products_info(message, marketplace_name)
