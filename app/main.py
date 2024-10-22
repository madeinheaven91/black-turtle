import asyncio
import locale
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import load_config
from middlewares.outer import LoggingMiddleware, TokenizerMiddleware
from utils import main_logger

from models import StudyEntityType
from api import *
from handlers import user_router, start_router

async def main():
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
    conf = load_config()
    print(
        r"""
 ____  _     ____  ____  _  __   _____  _     ____  _____  _     _____
/  _ \/ \   /  _ \/   _\/ |/ /  /__ __\/ \ /\/  __\/__ __\/ \   /  __/
| | //| |   | / \||  /  |   /     / \  | | |||  \/|  / \  | |   |  \  
| |_\\| |_/\| |-|||  \_ |   \     | |  | \_/||    /  | |  | |_/\|  /_ 
\____/\____/\_/ \|\____/\_|\_\    \_/  \____/\_/\_\  \_/  \____/\____\
    """
    )

    main_logger.critical(f"LOG LEVEL: {conf.app.log_level}")

    # Bot and dispatcher initialization
    bot = Bot(token=conf.bot.token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    # Router registration
    main_logger.critical("Registering routers")
    dp.include_router(user_router)
    dp.include_router(start_router)

    # Middleware registration
    main_logger.critical("Registering middlewares")
    dp.update.middleware(TokenizerMiddleware())
    dp.update.middleware(LoggingMiddleware())

    # Polling
    # await bot.delete_webhook(drop_pending_updates=True) # This skips all updates that were made when the bot was sleeping
    await dp.start_polling(bot)
    logging.shutdown()


if __name__ == "__main__":
    asyncio.run(main())


