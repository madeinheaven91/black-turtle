from typing import List
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from lexicon import LEXICON

router = Router()

@router.message(CommandStart())
async def handle_start(msg: Message):
    await msg.answer(LEXICON['/start'])

@router.message(F.text.lower().startswith('пары'))
async def handle_lessons(msg: Message, tokens: List[str]):
    # process_tokens()
    # request from api
    # transform request to message
    # send message
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
