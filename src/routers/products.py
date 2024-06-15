from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext


from src.states import (ProductsStatesGroup, AddNewArticulsStatesGroup)
from src.services.tg_document import (
    get_list_of_articuls_from_message_document,
    write_articuls_in_db
)
from src.keyboards import (
    main_manu_keyboard,
    load_products_keyboard,
    marketplaces_names_keyboard,
    extend_or_replace_articuls_keyboard
)
from src.enums import (
    ExtendOrReplaceArticulsEnum,
    MarketplaceNameEnum,
    CommonButtonsNames
)

from src.config import Settings

router = Router()


@router.message(
    AddNewArticulsStatesGroup.send_articuls,
    F.document,
)
async def load_document_message_handler(message: Message, state: FSMContext) -> None:
    try:
        articuls = await get_list_of_articuls_from_message_document(message)
    except ValueError:
        await message.answer('Документ имеет невалидное расширение')
    else:
        await message.answer('Документ успешно загружен! \nТеперь выберете маркетплейс, к которому вы бы хотели отнести данные артикулы', reply_markup=marketplaces_names_keyboard())
        await state.set_state(AddNewArticulsStatesGroup.choose_marketplace)
        await state.update_data({'articuls': articuls})


@router.message(
    AddNewArticulsStatesGroup.choose_marketplace,
    F.text.in_(
        [marketplace_name.value for marketplace_name in MarketplaceNameEnum])
)
async def choose_marketplace_message_handler(message: Message, state: FSMContext) -> None:
    marketplace_name = message.text
    await message.answer('Необходимо уточнить, вы хотите расширить или полностью заменить информацию о ранее существующих артикулах (если они есть)?', reply_markup=extend_or_replace_articuls_keyboard())
    await state.set_state(AddNewArticulsStatesGroup.extend_or_replace)
    await state.update_data({'marketplace_name': marketplace_name})


@router.message(
    AddNewArticulsStatesGroup.extend_or_replace,
    F.text.in_(
        [answer_option.value for answer_option in ExtendOrReplaceArticulsEnum])
)
async def extend_or_replace_articuls_message_handler(message: Message, state: FSMContext) -> None:
    answer_option = message.text
    state_data = await state.get_data()
    await write_articuls_in_db(message, answer_option, state_data)
    await message.answer('Артикулы были успешно записаны!', reply_markup=main_manu_keyboard())
    await state.clear()


@router.message(
    StateFilter(AddNewArticulsStatesGroup),
    F.text == CommonButtonsNames.BACK,
)
async def return_back_from_add_new_articuls_message_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text='Вы вернулись на главное меню', reply_markup=main_manu_keyboard())
    await state.clear()

# @router.message(
#     ProductsStatesGroup.get_products_list,
#     F.text == GetProductsStateEnums.GET_PRODUCTS_IN_TEXT,
# )
# async def get_link_to_products_in_text_message_handler(message: Message) -> None:
#     links = get_list_of_links_to_products(message)
#     for link in links:
#         await message.answer(link)

# @router.message(
#     ProductsStatesGroup.get_products_list,
#     F.text == GetProductsStateEnums.GET_PRODUCTS_IN_EXCEL,
# )
# async def get_excel_file_with_actual_product_prices_message_handler(message: Message) -> None:
#     await send_document_by_chat_id(message)

# @router.message(
#     ProductsStatesGroup.add_new_articuls,
#     F.text,
# )
# async def parse_articuls_from_text_message_handler(message: Message) -> None:
#     if not check_if_excel_by_chat_id_exists(message):
#         await message.answer('Ошибка! Файла с артикулами не существует!', reply_markup=load_products_keyboard())
#         return
#     add_new_articuls_in_excel_from_message(message)
#     await message.answer('Артикулы были успешно добавлены!', reply_markup=load_products_keyboard())


@router.message(
    ProductsStatesGroup.add_new_articuls,
)
async def all_other_messages_handler(message: Message) -> None:
    await message.answer('Сообщение не может быть обработано!\n'
                         'Отправьте Excel файл с артикулами товаров или перечисленные через запятую артикулы товаров сообщением!', reply_markup=load_products_keyboard())
