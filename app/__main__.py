import asyncio
import logging

from aiogram import Bot, Dispatcher 
from aiogram.client.default import DefaultBotProperties

# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from handlers import user_handlers
from config import Config, load_config
from middlewares.outer import LoggingMiddleware, TokenizerMiddleware
from utils.logger import logger


async def main():
    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')


    # Config and stuff
    config: Config = load_config()
    # engine = create_async_engine(url=config.db.url, echo=True)
    # session = async_sessionmaker(engine, expire_on_commit=False)
    #
    # Bot and dispatcher initialization
    bot = Bot(token=config.bot.token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()

    # Router registration
    logger.info('Registering routers')
    dp.include_router(user_handlers.router)

    # Middleware registration
    logger.info('Registering middleware')
    dp.update.middleware(LoggingMiddleware())
    dp.update.middleware(TokenizerMiddleware())

    # Polling
    # await bot.delete_webhook(drop_pending_updates=True) # This skips all updates that were made when the bot was sleeping
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
