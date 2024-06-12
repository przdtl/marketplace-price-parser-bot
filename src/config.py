from pydantic_settings import (BaseSettings, SettingsConfigDict)


class Settings(BaseSettings):

    BOT_TOKEN: str

    # MongoDB variables
    MONGODB_HOST: str
    MONGODB_PORT: str
    MONGODB_USER: str
    MONGODB_PASS: str

    # URL of site's products
    OZON_PRODUCT_URL: str = 'https://www.ozon.ru/product'

    # Prise parser variables
    PRICE_PARSER_SERVICE_URL: str = 'http://127.0.0.1:8000'
    OZON_PRICE_PARSER_SERVICE_URL: str = PRICE_PARSER_SERVICE_URL + '/ozon'
    WILDBERRIES_PRICE_PARSER_SERVICE_URL: str = PRICE_PARSER_SERVICE_URL + '/wildberries'

    @property
    def mongodb_dsn(self) -> str:
        return 'mongodb://{}:{}@{}:{}'.format(self.MONGODB_USER, self.MONGODB_PASS, self.MONGODB_HOST, self.MONGODB_PORT)

    model_config = SettingsConfigDict(env_file='.env')
