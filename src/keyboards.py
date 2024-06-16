from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.enums import (
    NonStateEnums,
    SettingsEnum,
    CommonButtonsNames,
    MarketplaceNameEnum,
    ExtendOrReplaceArticulsEnum,
    ProductsInfoExportWayEnum
)


def get_back_keyboard_button() -> KeyboardButton:
    return KeyboardButton(text=CommonButtonsNames.BACK)


def main_manu_keyboard() -> ReplyKeyboardMarkup:
    load_products = KeyboardButton(text=NonStateEnums.LOAD_PRODUCTS)
    get_products = KeyboardButton(text=NonStateEnums.GET_PRODUCTS)
    settings = KeyboardButton(text=NonStateEnums.SETTINGS)

    keyboard = [
        [load_products, get_products],
        [settings],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def settings_keyboard() -> ReplyKeyboardMarkup:
    setting_scraping_time = KeyboardButton(
        text=SettingsEnum.SET_SCRAPPING_TIME)
    back = get_back_keyboard_button()

    keyboard = [
        [setting_scraping_time],
        [back]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def export_products_ways_keyboard() -> ReplyKeyboardMarkup:
    back = get_back_keyboard_button()

    builder = ReplyKeyboardBuilder()
    export_way_buttons = []
    for export_way in ProductsInfoExportWayEnum:
        export_way_buttons.append(
            KeyboardButton(text=export_way.value))

    builder.row(*export_way_buttons, width=3)
    builder.add(back)

    markup = builder.as_markup()
    markup.resize_keyboard = True

    return markup


def load_products_keyboard() -> ReplyKeyboardMarkup:
    back = get_back_keyboard_button()

    keyboard = [
        [back],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def set_scrapping_time_keyboard() -> ReplyKeyboardMarkup:
    back = get_back_keyboard_button()

    keyboard = [
        [back],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def marketplaces_names_keyboard() -> ReplyKeyboardMarkup:
    back = get_back_keyboard_button()

    builder = ReplyKeyboardBuilder()
    marketplace_names_buttons = []
    for marketplace_name in MarketplaceNameEnum:
        marketplace_names_buttons.append(
            KeyboardButton(text=marketplace_name.value))

    builder.row(*marketplace_names_buttons, width=3)
    builder.add(back)

    markup = builder.as_markup()
    markup.resize_keyboard = True

    return markup


def extend_or_replace_articuls_keyboard() -> ReplyKeyboardMarkup:
    back = get_back_keyboard_button()

    builder = ReplyKeyboardBuilder()
    extend_or_replace_buttons = []
    for answer_option in ExtendOrReplaceArticulsEnum:
        extend_or_replace_buttons.append(
            KeyboardButton(text=answer_option.value))

    builder.row(*extend_or_replace_buttons, width=2)
    builder.add(back)

    markup = builder.as_markup()
    markup.resize_keyboard = True

    return markup
