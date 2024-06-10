from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)

from src.enums import (NonStateEnums, SettingsStateEnum,
                       GetProductsStateEnums, CommonButtonsNames)


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
        text=SettingsStateEnum.SET_SCRAPPING_TIME)
    back = get_back_keyboard_button()

    keyboard = [
        [setting_scraping_time],
        [back]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_products_keyboard() -> ReplyKeyboardMarkup:
    download_excel_document = KeyboardButton(
        text=GetProductsStateEnums.GET_PRODUCTS_IN_EXCEL)
    get_prodict_links = KeyboardButton(
        text=GetProductsStateEnums.GET_PRODUCTS_IN_TEXT)
    back = get_back_keyboard_button()

    keyboard = [
        [download_excel_document],
        [get_prodict_links],
        [back],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def load_products_keyboard() -> ReplyKeyboardMarkup:
    back = get_back_keyboard_button()

    keyboard = [
        [back],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
