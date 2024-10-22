from typing import List
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from sqlalchemy.orm import Session
from sqlalchemy import select, insert

from utils import main_logger
from lexicon import LEXICON
from keyboards import help_kb
from logic import process_lessons_tokens
from api import req_week, res_to_day, combine_simul, day_to_msg

user_router = Router()


@user_router.message(F.text.lower().startswith('пары'))
async def handle_lessons(msg: Message, tokens: List[str]):
    processed = process_lessons_tokens(tokens, msg.chat.id)
    # processed ['lessons', 'teacher' (kind), '1' (api_id), '21.09.24']

    kind = processed[1]
    id = processed[2]
    query_date = processed[3]
    res = req_week(kind, id, query_date)
    lessons = res_to_day(res, query_date)
    lessons = combine_simul(lessons)
    result = day_to_msg(lessons)
    await msg.answer(result)

@user_router.message(F.text.lower().startswith('помощь'))
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
    await msg.answer(result, reply_markup=help_kb)
