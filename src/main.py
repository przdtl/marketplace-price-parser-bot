import sys
import asyncio
import logging

from src.loader import dispatcher, bot
from src.routers.commands import router as commands_router
from src.routers.main_menu import router as main_menu_router
from src.routers.products import router as products_router
from src.routers.settings import router as settings_router


async def main() -> None:
    dispatcher.include_routers(
        products_router,
        main_menu_router,
        settings_router,
        commands_router
    )
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
