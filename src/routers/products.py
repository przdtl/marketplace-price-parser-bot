from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.states import (AddNewArticulsStatesGroup, GetProductsInfoStatesGroup)
from src.services.tg_document import (
    get_list_of_articuls_from_message_document,
    write_articuls_in_db,
    send_products_info
)
from src.keyboards import (
    main_manu_keyboard,
    marketplaces_names_keyboard,
    extend_or_replace_articuls_keyboard
)
from src.enums import (
    ExtendOrReplaceArticulsEnum,
    ProductsInfoExportWayEnum,
    MarketplaceNameEnum,
    CommonButtonsNames
)


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
async def choose_marketplace_by_adding_articuls_message_handler(message: Message, state: FSMContext) -> None:
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
    StateFilter(AddNewArticulsStatesGroup, GetProductsInfoStatesGroup),
    F.text == CommonButtonsNames.BACK,
)
async def return_back_from_add_new_articuls_message_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text='Вы вернулись на главное меню', reply_markup=main_manu_keyboard())
    await state.clear()


@router.message(
    GetProductsInfoStatesGroup.choose_export_type,
    F.text.in_(
        [export_way.value for export_way in ProductsInfoExportWayEnum])
)
async def choose_export_way_message_handler(message: Message, state: FSMContext) -> None:
    export_way = message.text
    await state.update_data({'export_way': export_way})
    await message.answer('Выберете маркетплейс, информацию о котором вы хотите получить', reply_markup=marketplaces_names_keyboard())
    await state.set_state(GetProductsInfoStatesGroup.choose_marketplace)


@ router.message(
    GetProductsInfoStatesGroup.choose_marketplace,
    F.text.in_(
        [marketplace_name.value for marketplace_name in MarketplaceNameEnum])
)
async def choose_marketplace_by_returning_products_info_message_handler(message: Message, state: FSMContext) -> None:
    marketplace_name = message.text
    state_data = await state.get_data()
    export_way = state_data.get('export_way')
    try:
        await send_products_info(message, marketplace_name, export_way)
    except ValueError:
        text = 'Ошибка! Вы не сохраняли информацию о товарах маркетплейста "{}"'.format(
            marketplace_name
        )
    else:
        text = 'Ваш документ!'
    finally:
        await message.answer(text, reply_markup=main_manu_keyboard())
        await state.clear()
