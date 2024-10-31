from .data import *
from .logger import main_logger
from .utils import lessons_declension
from .bot import bot, dp
from .lexicon import LEXICON

__all__ = [
    "main_logger",
    "admin_ids",
    "api_url",
    "req_headers",
    "relative_day_tokens",
    "absolute_day_tokens",
    "day_tokens",
    "week_tokens",
    "command_tokens",
    "lessons_declension",
    "bot",
    "dp",
    "LEXICON",
]
