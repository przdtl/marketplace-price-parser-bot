from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.enums import NonStateEnums
from src.states import (
    SettingsStatesGroup,
    AddNewArticulsStatesGroup,
    GetProductsInfoStatesGroup
)
from src.keyboards import (
    load_products_keyboard,
    settings_keyboard,
    export_products_ways_keyboard
)

router = Router()


@router.message(
    F.text == NonStateEnums.LOAD_PRODUCTS,
)
async def load_products_message_handler(message: Message, state: FSMContext) -> None:
    await message.answer('Вы перешли в меню загрузки информации о товарах', reply_markup=load_products_keyboard())
    await state.set_state(AddNewArticulsStatesGroup.send_articuls)


@router.message(
    F.text == NonStateEnums.GET_PRODUCTS,
)
async def get_products_message_handler(message: Message, state: FSMContext) -> None:
    await message.answer('Вы перешли в меню получения информации о товарах', reply_markup=export_products_ways_keyboard())
    await state.set_state(GetProductsInfoStatesGroup.choose_export_type)


@router.message(
    F.text == NonStateEnums.SETTINGS,
)
async def settings_message_handler(message: Message, state: FSMContext) -> None:
    await message.answer('Вы перешли в настройки', reply_markup=settings_keyboard())
    await state.set_state(SettingsStatesGroup.base_settings)
