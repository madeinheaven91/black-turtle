import asyncio
import logging
from datetime import date, timedelta

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import Config, load_config
from database.connect import engine
from database.tables import Base
from handlers import user_handlers
from middlewares.outer import LoggingMiddleware, TokenizerMiddleware
from sqlalchemy import text
from utils import main_logger

from models import StudyEntityType
from api import *

async def main():
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
    dp.include_router(user_handlers.router)

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


