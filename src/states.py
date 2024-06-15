from aiogram.fsm.state import StatesGroup, State


class ProductsStatesGroup(StatesGroup):
    add_new_articuls = State()
    get_products_list = State()


class SettingsStatesGroup(StatesGroup):
    base_settings = State()
    set_scraping_time = State()


class AddNewArticulsStatesGroup(StatesGroup):
    send_articuls = State()
    choose_marketplace = State()
    extend_or_replace = State()
