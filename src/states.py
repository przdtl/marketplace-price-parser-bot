from aiogram.fsm.state import StatesGroup, State


class SettingsStatesGroup(StatesGroup):
    base_settings = State()


class SetScrappingTime(StatesGroup):
    choose_marketplace = State()
    set_time = State()


class AddNewArticulsStatesGroup(StatesGroup):
    send_articuls = State()
    choose_marketplace = State()
    extend_or_replace = State()


class GetProductsInfoStatesGroup(StatesGroup):
    choose_export_type = State()
    choose_marketplace = State()
