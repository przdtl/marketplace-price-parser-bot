from aiogram import Bot, Dispatcher

from src.settings.config import Settings

bot = Bot(token=Settings().BOT_TOKEN)
dispatcher = Dispatcher()
