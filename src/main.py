import asyncio
from src.settings.loader import dispatcher, bot
from src.routers.commands import router as commands_router


async def main() -> None:
    dispatcher.include_router(commands_router)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
