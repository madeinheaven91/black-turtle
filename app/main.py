import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import Config, load_config
from database.connect import engine
from database.tables import Base
from handlers import user_handlers
from middlewares.outer import LoggingMiddleware, TokenizerMiddleware
from sqlalchemy import text
from utils.logger import logger


async def main():
    # Выводим в консоль информацию о начале запуска бота
    logger.info("Starting bot")

    # with engine.connect() as conn:
    #     result = conn.execute(text("SELECT * from chats;"))
    #     print(result)

    # Config and stuff
    config: Config = load_config()

    # Bot and dispatcher initialization
    bot = Bot(token=config.bot.token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    # Router registration
    logger.info("Registering routers")
    dp.include_router(user_handlers.router)

    # Middleware registration
    logger.info("Registering middleware")
    dp.update.middleware(LoggingMiddleware())
    dp.update.middleware(TokenizerMiddleware())

    # Polling
    # await bot.delete_webhook(drop_pending_updates=True) # This skips all updates that were made when the bot was sleeping
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
