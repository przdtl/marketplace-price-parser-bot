from enum import Enum


class CommonButtonsNames(str, Enum):
    BACK = 'Назад'


class NonStateEnums(str, Enum):
    LOAD_PRODUCTS = 'Загрузить'
    GET_PRODUCTS = 'Получить'
    SETTINGS = 'Настройки'


class SettingsStateEnum(str, Enum):
    SET_SCRAPPING_TIME = 'Установить время сканирования'


class ProductsInfoExportWayEnum(str, Enum):
    EXCEL = 'EXCEL'
    CSV = 'CSV'


class MarketplaceNameEnum(str, Enum):
    OZON = 'OZON'
    WILDBERRIES = 'WILDBERRIES'


class ExtendOrReplaceArticulsEnum(str, Enum):
    EXTEND = 'Расширить'
    REPLACE = 'Заменить'
