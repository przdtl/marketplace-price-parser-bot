from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.states import SettingsStatesGroup
from src.enums import SettingsStateEnum, CommonButtonsNames
from src.keyboards import main_manu_keyboard

router = Router()


@router.message(
    SettingsStatesGroup.base_settings,
    F.text == SettingsStateEnum.SET_SCRAPPING_TIME,
)
async def base_settings_message_handler(message: Message, state: FSMContext) -> None:
    await message.answer('Вы перешли в настройку времени сканирования цен')
    await state.set_state(SettingsStatesGroup.set_scraping_time)


@router.message(
    StateFilter(
        SettingsStatesGroup.base_settings,
    ),
    F.text == CommonButtonsNames.BACK,
)
async def return_back_message_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text='Вы вернулись на главное меню', reply_markup=main_manu_keyboard())
    await state.clear()
