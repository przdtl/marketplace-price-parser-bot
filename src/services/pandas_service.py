import pandas as pd

from aiogram.types import Message
from pandas.core.series import Series

from src.config import Settings
from src.services.excel_services import (
    get_excel_filename_by_chat_id, get_product_prices_by_articuls)


pd.options.mode.chained_assignment = None


def read_dataframe_from_excel(path_to_document: str) -> pd.DataFrame:
    '''Возвращает объект DataFrame excel по переданному пути'''
    df = pd.read_excel(io=path_to_document, header=None, index_col=None)

    return df


def write_dataframe_to_excel(df: pd.DataFrame, path_to_document: str) -> None:
    '''Запись объекта DataFrame в Excel файл'''
    df.to_excel(path_to_document, index=False, header=False)


def get_product_articuls_from_excel(df: pd.DataFrame) -> list[int]:
    '''Возвращает список артикулов, считанных из объекта DataFrame'''
    df_list = list(df[0].tolist())

    return df_list


def add_new_empty_column_in_dataframe(df: pd.DataFrame) -> None:
    '''Добавляет новый пустой столбик в объект DataFrame'''
    df.insert(len(df.columns), len(df.columns), float('nan'))


def add_new_price_to_dataframe_row(df: pd.DataFrame, row: Series, new_price: float) -> None:
    '''Добавляет новую цену в строку DataFrame если она изменилась'''
    columns_count = len(df.columns)
    index_of_last_non_nan_elem = row.count() - 1
    last_price = row[index_of_last_non_nan_elem] if index_of_last_non_nan_elem > 0 else -1

    if (new_price == -1) or (last_price == new_price):
        return

    if index_of_last_non_nan_elem + 1 == columns_count:
        add_new_empty_column_in_dataframe(df)

    df[index_of_last_non_nan_elem + 1][row.name] = new_price


def update_prices_dataframe(df: pd.DataFrame, new_prices: list[float]) -> None:
    '''Проходит по всем строкам объекта DataFrame и обновляет цены на товары'''
    print(new_prices)
    for index, row in df.iterrows():
        add_new_price_to_dataframe_row(df, row, new_prices[index])


async def get_new_prices_by_products_articuls_and_update_it_in_dataframe(df: pd.DataFrame) -> None:
    '''Получает артикуры товаров из таблицы DataFrame, цены на эти товары и обновлет цены в таблице DataFrame'''
    articuls = get_product_articuls_from_excel(df)
    new_prices = await get_product_prices_by_articuls(*articuls)
    update_prices_dataframe(df, new_prices)


async def read_excel_and_write_new_prices(path_to_document: str) -> None:
    '''Читает документ Excel, образуя из него таблицу DataFrame, записывает туда новые цены на товары и сохраняет на диске'''
    df = read_dataframe_from_excel(path_to_document)
    await get_new_prices_by_products_articuls_and_update_it_in_dataframe(df)
    write_dataframe_to_excel(df, path_to_document)


def parse_valid_ozon_articuls_from_str(message: str) -> list[int]:
    splitted_articuls = message.split(',')
    articuls = []
    for articul in splitted_articuls:
        try:
            articul = int(articul.strip())

        except ValueError:
            pass

        else:
            articuls.append(articul)

    return articuls


def delete_existing_articuls(existing_articuls: list[int], new_articuls: list[int]) -> list[int]:
    articuls = [x for x in new_articuls if x not in existing_articuls]

    return articuls


def write_articuls_in_dataframe(df: pd.DataFrame, *articuls: int) -> None:
    new_df_rows = pd.DataFrame(
        [[articul] for articul in articuls]
    )
    df = pd.concat([df, new_df_rows], ignore_index=True)


def add_new_articuls_in_dataframe(df: pd.DataFrame, new_articuls: list[int]) -> None:
    existing_articuls = get_product_articuls_from_excel(df)
    new_articuls = delete_existing_articuls(existing_articuls, new_articuls)
    write_articuls_in_dataframe(df, *new_articuls)


def open_excel_and_write_new_articuls_from_message(path_to_document: str, message: str) -> None:
    df = read_dataframe_from_excel(path_to_document)
    articuls = parse_valid_ozon_articuls_from_str(message)
    add_new_articuls_in_dataframe(df, articuls)


def add_new_articuls_in_excel_from_message(message: Message) -> None:
    path_to_document = get_excel_filename_by_chat_id(message)
    open_excel_and_write_new_articuls_from_message(
        path_to_document, message.text
    )


def get_links_to_products_by_articuls(*articuls: int) -> list[str]:
    url_to_products = Settings().OZON_PRODUCT_URL
    links = []
    for articul in articuls:
        links.append(url_to_products + str(articul))

    return links


def get_list_of_links_from_dataframe(df: pd.DataFrame) -> list[str]:
    articuls = get_product_articuls_from_excel(df)
    links = get_links_to_products_by_articuls(*articuls)

    return links


def open_excel_and_get_list_of_links(path_to_document: str) -> list[str]:
    df = read_dataframe_from_excel(path_to_document)
    links = get_list_of_links_from_dataframe(df)

    return links


def get_list_of_links_to_products(message: Message) -> list[str]:
    path_to_document = get_excel_filename_by_chat_id(message)
    links = open_excel_and_get_list_of_links(path_to_document)

    return links
