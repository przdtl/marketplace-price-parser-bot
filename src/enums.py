from enum import Enum


class CommonButtonsNames(str, Enum):
    BACK = 'Назад'


class NonStateEnums(str, Enum):
    LOAD_PRODUCTS = 'Загрузить'
    GET_PRODUCTS = 'Получить'
    SETTINGS = 'Настройки'


class SettingsStateEnum(str, Enum):
    SET_SCRAPPING_TIME = 'Установить время сканирования'


class GetProductsStateEnums(str, Enum):
    GET_PRODUCTS_IN_TEXT = 'Получить инормацию сообщением'
    GET_PRODUCTS_IN_EXCEL = 'Получить информациею в Excel'


class LoadProductsStateEnums(str, Enum):
    pass


class MarketplaceNameEnum(str, Enum):
    OZON = 'OZON'
    WILDBERRIES = 'WILDBERRIES'


class ExtendOrReplaceArticulsEnum(str, Enum):
    EXTEND = 'Расширить'
    REPLACE = 'Заменить'
