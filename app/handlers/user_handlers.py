from typing import List
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
# from app.filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
# from app.keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    # create_edit_keyboard)
# from app.keyboards.pagination_kb import create_pagination_keyboard
from lexicon import LEXICON
# from app.services.file_handling import book

# from app.database import Database

router = Router()

@router.message(CommandStart())
async def handle_start(msg: Message):
    await msg.answer(LEXICON['/start'])

@router.message(F.text.lower().startswith('пары'))
async def handle_lessons(msg: Message, tokens: List[str]):
    result = "not implemented yet"
    await msg.answer(result)

@router.message(F.text.lower().startswith('помощь'))
async def handle_help(msg: Message, tokens: List[str]):
    match tokens[1]:
        case 'пары':
            result = LEXICON['help_lessons']
        case 'фио':
            result = LEXICON['help_fio']
        case 'звонки':
            result = LEXICON['help_bells']
        case _:
            result = LEXICON['help_generic']
    await msg.answer(result)
