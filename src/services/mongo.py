import asyncio

from src.database import db

collection = db.document_collection


async def add_list_of_products_in_document(chat_id: int, marketplace_name: str, articuls: list[int]) -> None:
    '''Создаёт записи о переданных товарах в базе данных'''
    document_record = []

    articles_not_present = await get_not_existed_articuls(
        chat_id, marketplace_name, articuls)

    if not articles_not_present:
        return

    for articul in articles_not_present:
        document_record.append({
            'chat_id': chat_id,
            'articul': articul,
            'marketplace_name': marketplace_name,
            'prices': [],
        })

    await collection.insert_many(document_record)


async def delete_all_products_from_user_in_specific_marketplace(chat_id: int, marketplace_name: str) -> None:
    '''Удаляет все записи о товарах у пользователя в конкретном маркетплейсе'''
    user_filter = {
        'chat_id': chat_id,
        'marketplace_name': marketplace_name,
    }
    await collection.delete_one(user_filter)


async def get_all_users_articuls_of_specific_marketplace(chat_id: int, marketplace_name: str) -> list[int]:
    '''Возвращает список артикулов у конкретного пользователя по желаемому маркетплейсу'''
    product_filter = {
        'chat_id': chat_id,
        'marketplace_name': marketplace_name,
    }
    articuls_projection = {
        'articul': True,
        '_id': False
    }
    articuls_cursor = collection.find(product_filter, articuls_projection)
    list_of_articuls_objects = await articuls_cursor.to_list(None)
    list_of_articuls = [obj['articul'] for obj in list_of_articuls_objects]

    return list_of_articuls


async def get_not_existed_articuls(chat_id: int, marketplace_name: str, articuls: list[int]) -> list[int]:
    '''Проверяет переданные артикулы на существование в БД и возвращает только те, которых там не существует'''
    existence_articuls = await get_all_users_articuls_of_specific_marketplace(
        chat_id, marketplace_name)
    result_articuls = [
        articul for articul in articuls if articul not in existence_articuls]

    return result_articuls


async def get_all_users_articuls_and_its_prices_of_specific_marketplace(chat_id: int, marketplace_name: str) -> dict[int, list[float]]:
    '''
    Возвращает словарь данных о ценах товаров по их артикулам

    Returns:
        dict[int, list[float]]: Словарь типа {<артикул>: [<цены>], ...}
    '''
    product_filter = {
        'chat_id': chat_id,
        'marketplace_name': marketplace_name,
    }
    products_projection = {
        'articul': True,
        'prices': True,
        '_id': False
    }
    products_cursor = collection.find(product_filter, products_projection)
    list_of_products_objects = await products_cursor.to_list(None)
    dict_of_products = {obj['articul']: obj['prices']
                        for obj in list_of_products_objects}
    return dict_of_products


async def get_product_prices_from_user_from_specific_marketplace_by_articul(chat_id: int, marketplace_name: str, articul: int) -> list[float]:
    '''Возвращает список цен конкретного товара'''
    product_filter = {
        'chat_id': chat_id,
        'articul': articul,
        'marketplace_name': marketplace_name,
    }
    prices = await collection.find_one(product_filter)

    return prices['prices'] if prices else []
