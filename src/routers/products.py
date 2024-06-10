from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext


from src.states import ProductsStatesGroup
from src.services.excel_services import (
    get_document_from_message_and_download_if_extention_is_excel,
    check_if_excel_by_chat_id_exists,
    send_document_by_chat_id,
)
from src.services.pandas_service import (
    add_new_articuls_in_excel_from_message,
    get_list_of_links_to_products,
)
from src.keyboards import (main_manu_keyboard, load_products_keyboard)
from src.enums import (GetProductsStateEnums, CommonButtonsNames)

router = Router()


@router.message(
    ProductsStatesGroup.add_new_articuls,
    F.document,
)
async def load_new_excel_file_with_articuls_message_handler(message: Message) -> None:
    path_to_document = await get_document_from_message_and_download_if_extention_is_excel(
        message,
    )

    if not path_to_document:
        await message.answer('Документ не может быть сохранён!')
    else:
        await message.answer('Документ был успешно сохранён!')


@router.message(
    ProductsStatesGroup.get_products_list,
    F.text == GetProductsStateEnums.GET_PRODUCTS_IN_TEXT,
)
async def get_link_to_products_in_text_message_handler(message: Message) -> None:
    links = get_list_of_links_to_products(message)

    for link in links:
        await message.answer(link)


@router.message(
    ProductsStatesGroup.get_products_list,
    F.text == GetProductsStateEnums.GET_PRODUCTS_IN_EXCEL,
)
async def get_excel_file_with_actual_product_prices_message_handler(message: Message) -> None:
    await send_document_by_chat_id(message)


@router.message(
    StateFilter(ProductsStatesGroup.get_products_list,
                ProductsStatesGroup.add_new_articuls),
    F.text == CommonButtonsNames.BACK,
)
async def return_back_message_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text='Вы вернулись на главное меню', reply_markup=main_manu_keyboard())
    await state.clear()


@router.message(
    ProductsStatesGroup.add_new_articuls,
    F.text,
)
async def parse_articuls_from_text_message_handler(message: Message) -> None:
    if not check_if_excel_by_chat_id_exists(message):
        await message.answer('Ошибка! Файла с артикулами не существует!', reply_markup=load_products_keyboard())
        return

    add_new_articuls_in_excel_from_message(message)
    await message.answer('Артикулы были успешно добавлены!', reply_markup=load_products_keyboard())


@router.message(
    ProductsStatesGroup.add_new_articuls,
)
async def all_other_messages_handler(message: Message) -> None:
    await message.answer('Сообщение не может быть обработано!\n'
                         'Отправьте Excel файл с артикулами товаров или перечисленные через запятую артикулы товаров сообщением!', reply_markup=load_products_keyboard())
