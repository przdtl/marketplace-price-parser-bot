import io

import pandas as pd

from src.services.mongo import get_all_users_articuls_and_its_prices_of_specific_marketplace


def read_first_column_dataframe_from_excel(path_to_document: str) -> pd.DataFrame:
    '''Возвращает DataFrame по первому столбцу, считанному из Excel файла по переданному пути'''
    df = pd.read_excel(io=path_to_document, header=None,
                       index_col=None, usecols=[0])

    return df


def read_first_column_dataframe_from_csv(path_to_document: str) -> pd.DataFrame:
    '''Возвращает DataFrame по первому столбцу, считанному из CSV файла по переданному пути'''
    df = pd.read_csv(filepath_or_buffer=path_to_document, header=None,
                     index_col=None, usecols=[0])

    return df


def get_list_of_first_column_dataframe(df: pd.DataFrame) -> list[int]:
    '''Возвращает список из элементов первого столбца объекта DataFrame'''
    df_list = list(set(df[0].tolist()))

    return df_list


def get_excel_bytestr_from_dataframe(df: pd.DataFrame) -> bytes:
    '''Преобразует объект DataFrame в байтовую строку Excel без сохранения на диск'''
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, header=False)
    writer.close()
    xlsx_bytes_data = output.getvalue()

    return xlsx_bytes_data


def get_csv_bytestr_from_dataframe(df: pd.DataFrame) -> bytes:
    '''Преобразует объект DataFrame в байтовую строку CSV без сохранения на диск'''
    output = io.BytesIO()
    df.to_csv(output, index=False, header=False)
    csv_bytes_data = output.getvalue()

    return csv_bytes_data


async def get_table_of_articuls_and_its_prices(chat_id: int, marketplace_name: str) -> pd.DataFrame:
    '''Получает словарь данных о ценах товаров по их артикулам и конвертирует его в матрицу для удобного ввода в объект ``DataFrame``'''
    table = []
    dict_of_products = await get_all_users_articuls_and_its_prices_of_specific_marketplace(
        chat_id, marketplace_name)
    for articul, prices in dict_of_products.items():
        row = [articul]
        row.extend(prices)
        table.append(row)

    return pd.DataFrame(table)
