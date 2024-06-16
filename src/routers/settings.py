import re

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.states import SettingsStatesGroup, SetScrappingTime
from src.enums import CommonButtonsNames, SettingsEnum, MarketplaceNameEnum
from src.keyboards import (
    main_manu_keyboard,
    marketplaces_names_keyboard,
    set_scrapping_time_keyboard
)
from src.services.tg_document import set_time_of_products_pricrs_parsing

router = Router()


@router.message(
    SettingsStatesGroup.base_settings,
    F.text == SettingsEnum.SET_SCRAPPING_TIME,
)
async def choose_set_scrapping_time_in_settings_message_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(SetScrappingTime.choose_marketplace)
    await message.answer('Выберете маркетплейс, время сканирования которого хотите установить', reply_markup=marketplaces_names_keyboard())


@router.message(
    SetScrappingTime.choose_marketplace,
    F.text.in_(
        [marketplace_name.value for marketplace_name in MarketplaceNameEnum]),
)
async def choose_marketplace_by_setting_scrapping_time_message_handler(message: Message, state: FSMContext) -> None:
    marketplace_name = message.text
    await message.answer('Введите время сканирования формата часы:минуты:секунды (по МСК))', reply_markup=set_scrapping_time_keyboard())
    await state.set_state(SetScrappingTime.set_time)
    await state.update_data({'marketplace_name': marketplace_name})


@router.message(
    SetScrappingTime.set_time,
    F.text.regexp(r'(\d{1,2}):(\d{1,2}):(\d{1,2})')
)
async def set_scrapping_time_message_handler(message: Message, state: FSMContext) -> None:
    parse_time_match = re.match(r'(\d{1,2}):(\d{1,2}):(\d{1,2})', message.text)
    hour = parse_time_match[1]
    minute = parse_time_match[2]
    second = parse_time_match[3]
    state_data = await state.get_data()
    marketplace_name = state_data.get('marketplace_name')

    status_code = await set_time_of_products_pricrs_parsing(
        chat_id=message.chat.id,
        marketpalce_name=marketplace_name,
        hour=hour,
        minute=minute,
        second=second,
    )

    match status_code:
        case status_code if 400 <= status_code < 500:
            await message.answer('Вы ввели некорректные данные! Попробуйте ещё раз.')
        case status_code if 500 <= status_code:
            await message.answer('Произошла ошибка на сервере! Попробуйте позже.', reply_markup=main_manu_keyboard())
            await state.clear()
        case _:
            await message.answer('Время сканирования успешно установлено!', reply_markup=main_manu_keyboard())
            await state.clear()


@router.message(
    StateFilter(SettingsStatesGroup, SetScrappingTime),
    F.text == CommonButtonsNames.BACK,
)
async def return_back_message_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text='Вы вернулись на главное меню', reply_markup=main_manu_keyboard())
    await state.clear()
