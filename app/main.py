import asyncio
import locale
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import load_config
from middlewares import LoggingMiddleware, TokenizerMiddleware, ValidateMiddleware, ErrorHandlingMiddleware, AdminCheckMiddleware
from shared import main_logger, bot, dp, LEXICON
from handlers import user_router, start_router, admin_router
from sqlalchemy.orm import Session
from database import engine, Admin

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
    admin_router.message.middleware(AdminCheckMiddleware())
    dp.update.middleware(ValidateMiddleware())
    dp.message.middleware(TokenizerMiddleware())
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(ErrorHandlingMiddleware())

    with Session(engine) as session:
        owners = session.query(Admin).filter(Admin.level == 5).all()
        for owner in owners:
            await bot.send_message(owner.id, "Бот включен")
    # Polling
    # await bot.delete_webhook(drop_pending_updates=True) # This skips all updates that were made when the bot was sleeping
    await dp.start_polling(bot)
    logging.shutdown()
    with Session(engine) as session:
        owners = session.query(Admin).filter(Admin.level == 5).all()
        for owner in owners:
            await bot.send_message(owner.id, "Бот выключен")


if __name__ == "__main__":
    asyncio.run(main())



