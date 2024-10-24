import asyncio
import locale
import logging

from config import load_config
from middlewares.outer import LoggingMiddleware, TokenizerMiddleware, ValidateMiddleware
from shared import main_logger, bot, dp
from handlers import user_router, start_router, admin_router

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


    # Router registration
    main_logger.critical("Registering routers")
    dp.include_router(user_router)
    dp.include_router(start_router)
    dp.include_router(admin_router)

    # Middleware registration
    main_logger.critical("Registering middlewares")
    dp.update.middleware(ValidateMiddleware())
    dp.message.middleware(TokenizerMiddleware())
    dp.message.middleware(LoggingMiddleware())

    # Polling
    # await bot.delete_webhook(drop_pending_updates=True) # This skips all updates that were made when the bot was sleeping
    await dp.start_polling(bot)
    logging.shutdown()


if __name__ == "__main__":
    asyncio.run(main())


