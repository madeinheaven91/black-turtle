import asyncio
import locale
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import load_config
from middlewares.outer import LoggingMiddleware, TokenizerMiddleware, ValidateMiddleware, ErrorHandlingMiddleware
from shared import main_logger, bot, dp, LEXICON
from handlers import user_router, start_router, admin_router

async def main():
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
    conf = load_config()
    print(LEXICON["ascii_art"])

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
    dp.message.middleware(ErrorHandlingMiddleware())

    # Polling
    # await bot.delete_webhook(drop_pending_updates=True) # This skips all updates that were made when the bot was sleeping
    await dp.start_polling(bot)
    logging.shutdown()


if __name__ == "__main__":
    asyncio.run(main())



