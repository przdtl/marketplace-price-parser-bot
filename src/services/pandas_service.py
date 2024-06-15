import io
import pandas as pd

from typing import Union

from src.services.mongo import get_all_users_articuls_and_its_prices_of_specific_marketplace

pd.options.mode.chained_assignment = None


def read_first_column_dataframe_from_excel(path_to_document: str) -> pd.DataFrame:
    '''Возвращает DataFrame по первому столбцу, считанному из Excel файла по переданному пути'''
    df = pd.read_excel(io=path_to_document, header=None,
                       index_col=None, usecols=[0])

    return df


def read_first_column_dataframe_from_csv(path_to_document: str) -> pd.DataFrame:
    '''Возвращает DataFrame по первому столбцу, считанному из CSV файла по переданному пути'''
    df = pd.read_csv(io=path_to_document, header=None,
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


# def parse_valid_ozon_articuls_from_str(message: str) -> list[int]:
#     splitted_articuls = message.split(',')
#     articuls = []
#     for articul in splitted_articuls:
#         try:
#             articul = int(articul.strip())

#         except ValueError:
#             pass

#         else:
#             articuls.append(articul)

#     return articuls

# def delete_existing_articuls(existing_articuls: list[int], new_articuls: list[int]) -> list[int]:
#     articuls = [x for x in new_articuls if x not in existing_articuls]

#     return articuls

# def get_links_to_products_by_articuls(*articuls: int) -> list[str]:
#     url_to_products = Settings().OZON_PRODUCT_URL
#     links = []
#     for articul in articuls:
#         links.append(url_to_products + str(articul))

#     return links
