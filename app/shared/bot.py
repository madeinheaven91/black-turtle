from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from app.config import load_config
from app.shared import main_logger

conf = load_config()

bot = Bot(token=conf.bot.token, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
