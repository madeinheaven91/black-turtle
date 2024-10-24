from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from config import load_config
from shared import main_logger

conf = load_config()

bot = Bot(token=conf.bot.token, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
