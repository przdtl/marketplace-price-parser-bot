from pathlib import Path
from pydantic_settings import (BaseSettings, SettingsConfigDict)


class Settings(BaseSettings):

    BOT_TOKEN: str
    PATH_TO_EXCEL_FOLDER: str = Path(__file__).resolve().parent + 'media/excel'

    model_config = SettingsConfigDict(env_file='.env')
