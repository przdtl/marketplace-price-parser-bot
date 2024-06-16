import logging

from aiogram import Bot, Dispatcher

from config import Settings

bot = Bot(token=Settings().BOT_TOKEN)
dispatcher = Dispatcher()
