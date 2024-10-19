from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from app.filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from app.keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from app.keyboards.pagination_kb import create_pagination_keyboard
from app.lexicon import LEXICON
from app.services.file_handling import book

from app.database import Database

router = Router()

    
